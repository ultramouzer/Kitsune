import sys
sys.setrecursionlimit(100000)

import re
import config
import requests
import cloudscraper
import uuid
import json
import datetime
from bs4 import BeautifulSoup
from os.path import join
from os import makedirs

from flask import current_app

from ..internals.database.database import get_conn
from ..lib.artist import index_artists, is_artist_dnp
from ..lib.post import remove_post_if_flagged_for_reimport, post_exists
from ..lib.download import download_file, DownloaderException
from ..lib.proxy import get_proxy

def import_posts(log_id, key, offset = 1):
    makedirs(join(config.download_path, 'logs'), exist_ok=True)
    conn = get_conn()

    try:
        scraper = cloudscraper.create_scraper().get(
            f"https://gumroad.com/discover_search?from={offset}&user_purchases_only=true",
            cookies = { '_gumroad_app_session': key },
            proxies=get_proxy()
        )
        scraper_data = scraper.json()
        scraper.raise_for_status()
    except requests.HTTPError:
        current_app.logger.exception(f'Error: Status code {scraper_data.status_code} when contacting Gumroad API.')
        return

    if (scraper_data['total'] > 100000):
        current_app.logger.(f'Error: Can\'t log in; is your session key correct?')

    soup = BeautifulSoup(scraper_data['products_html'], 'html.parser')
    products = soup.find_all(class_='product-card')
	
    user_id = None

    for product in products:
        post_id = product['data-permalink']
        purchase_id = product.find(class_='js-product')['data-purchase-id']
        title = product.select_one('.description-container h1 strong').string
        user_id_element = product.find(class_='preview-container')['data-asset-previews']
        user_id_nums = re.findall(r"\d+", user_id_element)
        user_id = list(filter(lambda el: len(el) == 13, user_id_nums))[0]

        file_directory = f"files/gumroad/{user_id}/{post_id}"
        attachments_directory = f"attachments/gumroad/{user_id}/{post_id}"

        if is_artist_dnp('gumroad', user_id):
            current_app.logger.debug(f"[{import_id}]: Skipping post {post_id} from user {user_id} is in do not post list")
            continue

        remove_post_if_flagged_for_reimport('gumroad', user_id, post_id)

        if post_exists('gumroad', user_id, post_id):
            current_app.logger.debug(f'[{import_id}]: Skipping post {post_id} from user {user_id} because already exists')
            continue

        print(f"Starting import: {post_id}")

        post_model = {
            'id': post_id,
            '"user"': user_id,
            'service': 'gumroad',
            'title': title,
            'content': '',
            'embed': {},
            'shared_file': False,
            'added': datetime.datetime.now(),
            'published': None,
            'edited': None,
            'file': {},
            'attachments': []
        }
        
        scraper2 = cloudscraper.create_scraper().get(
            f"https://gumroad.com/library/purchases/{purchase_id}",
            cookies = { '_gumroad_app_session': key },
            proxies=get_proxy()
        )
        scraper_data2 = scraper2.text
        soup2 = BeautifulSoup(scraper_data2, 'html.parser')
        content_url = soup2.select_one('.button.button-primary.button-block')['href']

        scraper3 = cloudscraper.create_scraper().get(
            content_url,
            cookies = { '_gumroad_app_session': key },
            proxies=get_proxy()
        )
        scraper_data3 = scraper3.text
        soup3 = BeautifulSoup(scraper_data3, 'html.parser')
        thumbnail1 = soup3.select_one('.image-preview-container img').get('src') if soup3.select_one('.image-preview-container img') else None
        thumbnail2 = soup3.select_one('.image-preview-container img').get('data-cfsrc') if soup3.select_one('.image-preview-container img') else None
        thumbnail3 = soup3.select_one('.image-preview-container noscript img').get('src') if soup3.select_one('.image-preview-container noscript img') else None
        try:
            download_data = json.loads(soup3.select_one('div[data-react-class="DownloadPage/FileList"]')['data-react-props'])
        except:
            download_data = {
              "files": [],
              "download_info": {}
            }

        thumbnail = thumbnail1 or thumbnail2 or thumbnail3
        if thumbnail:
            filename, _ = download_file(
                join(config.download_path, file_directory),
                thumbnail
            )
            post_model['file']['name'] = filename
            post_model['file']['path'] = f'/{file_directory}/{filename}'

        for _file in download_data['files']:
            filename, _ = download_file(
                join(config.download_path, attachments_directory),
                'https://gumroad.com' + download_data['download_info'][_file['id']]['download_url'],
                name = f'{_file["file_name"]}.{_file["extension"].lower()}',
                cookies = { '_gumroad_app_session': key }
            )
            post_model['attachments'].append({
                'name': filename,
                'path': f'/{attachments_directory}/{filename}'
            })

        post_model['embed'] = json.dumps(post_model['embed'])
        post_model['file'] = json.dumps(post_model['file'])
        for i in range(len(post_model['attachments'])):
            post_model['attachments'][i] = json.dumps(post_model['attachments'][i])

        columns = post_model.keys()
        data = ['%s'] * len(post_model.values())
        data[-1] = '%s::jsonb[]' # attachments
        query = "INSERT INTO posts ({fields}) VALUES ({values})".format(
            fields = ','.join(columns),
            values = ','.join(data)
        )
        cursor = conn.cursor()
        cursor.execute(query, list(post_model.values()))
        conn.commit()

        current_app.logger.debug(f"[{import_id}]: Finished importing post {post_id} from user {user_id}!")

    if len(products):
        next_offset = offset + scraper_data['result_count']
        current_app.logger.debug(f'[{import_id}]: Finished processing offset {offset}. Importing offset {next_offset}')
        import_posts(log_id, key, offset=next_offset)
    else:
        current_app.logger.debug(f"[{import_id}]: Finished scanning for posts.")
        index_artists()

    return_conn(conn)

if __name__ == '__main__':
    if len(sys.argv) > 1:
        import_posts(str(uuid.uuid4()), sys.argv[1])
    else:
        print('Argument required - Login token')
