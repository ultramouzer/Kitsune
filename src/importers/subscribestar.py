import sys
import datetime
import config
import json
import uuid
import requests
from os.path import join
from io import StringIO
from html.parser import HTMLParser
from bs4 import BeautifulSoup
import os
from urllib.parse import urlparse
import dateparser

from flask import current_app

from ..internals.database.database import get_conn, get_raw_conn, return_conn
from ..lib.artist import index_artists, is_artist_dnp, update_artist, delete_artist_cache_keys
from ..lib.post import post_flagged, post_exists, delete_post_flags, move_to_backup, restore_from_backup, delete_backup
from ..lib.autoimport import encrypt_and_save_session_for_auto_import, kill_key
from ..internals.utils.download import download_file, DownloaderException
from ..internals.utils.scrapper import create_scrapper_session
from ..internals.utils.proxy import get_proxy
from ..internals.utils.logger import log
from ..internals.utils.utils import parse_date

class MLStripper(HTMLParser):
    def __init__(self):
        super().__init__()
        self.reset()
        self.strict = False
        self.convert_charrefs= True
        self.text = StringIO()
    def handle_data(self, d):
        self.text.write(d)
    def get_data(self):
        return self.text.getvalue()

def strip_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()

def import_posts(import_id, key, contributor_id, allowed_to_auto_import, key_id):
    jar = requests.cookies.RequestsCookieJar()
    jar.set('auth_token', key)
    try:
        scraper = create_scrapper_session(useCloudscraper=True).get(
            "https://subscribestar.adult/phd14517a.json",
            cookies=jar,
            proxies=get_proxy()
        )
        scraper_data = scraper.json()['html']
        scraper.raise_for_status()
    except requests.HTTPError as exc:
        log(import_id, f'Status code {exc.response.status_code} when contacting SubscribeStar API.', 'exception')
        return

    if scraper_data == "":
        log(import_id, f"No active subscriptions or invalid key. No posts will be imported.")
        return #break early as there's nothing anyway
    
    first_run = True
    while True:
        soup = BeautifulSoup(scraper_data, 'html.parser')
        posts = soup.find_all("div", {"class": "post"})
        if (first_run and len(posts) == 0):
            if (key_id):
                kill_key(key_id)
        else:
            if (allowed_to_auto_import):
                try:
                    encrypt_and_save_session_for_auto_import('subscribestar', key, contributor_id = contributor_id)
                    log(import_id, f"Your key was successfully enrolled in auto-import!", to_client = True)
                except:
                    log(import_id, f"An error occured while saving your key for auto-import.", 'exception')
        
        first_run = False
        for post in posts:
            try:
                post_id = post['data-id']
                user_id = post.find("a", {"class": "post-avatar"})['href'].replace('/', '')

                if "is-locked" in post.find("div", {"class": "post-body"})['class']:
                    log(import_id, f"Skipping post {post_id} from user {user_id} as tier is too high")
                    continue

                if is_artist_dnp('subscribestar', user_id):
                    log(import_id, f"Skipping post {post_id} from user {user_id} is in do not post list")
                    continue

                if post_exists('subscribestar', user_id, str(post_id)) and not post_flagged('subscribestar', user_id, str(post_id)):
                    log(import_id, f'Skipping post {post_id} from user {user_id} because already exists')
                    continue

                log(import_id, f"Starting import: {post_id}")
                #post_data = post.find("div", {"class": "trix-content"})
                post_data = post.find("div", {"class": "post-content"})
                # content = ""
                # for elem in post_data.recursiveChildGenerator():
                #     if isinstance(elem, str):
                #         content += elem.strip()
                #     elif elem.name == 'br':
                #         content += '\n'
                
                stripped_content = strip_tags(post_data.text)
                date = post.find("div", {"class": "post-date"}).a.get_text()
                parsed_date = dateparser.parse(date.replace("DOPOLEDNE", "AM").replace("ODPOLEDNE", "PM")) #Workaround for the Czeck langage

                post_model = {
                    'id': str(post_id),
                    '"user"': user_id,
                    'service': 'subscribestar',
                    'title': (stripped_content[:60] + '..') if len(stripped_content) > 60 else stripped_content,
                    'content': str(post_data),
                    'embed': {},
                    'shared_file': False,
                    'added': datetime.datetime.now(),
                    'published': parsed_date,
                    'edited': None,
                    'file': {},
                    'attachments': []
                }

                post_attachment_field = post.find("div", {"class": "uploads"})
                if post_attachment_field: #if posts has any kind of attachement
                    image_attachments = post_attachment_field.find("div", {"class": "uploads-images"})
                    docs_attachments = post_attachment_field.find("div", {"class": "uploads-docs"})

                    if image_attachments:
                        for attachment in json.loads(image_attachments['data-gallery']):
                            name = os.path.basename( urlparse(attachment['url']).path ) #gets the filename from the url
                            #download the file
                            reported_filename, hash_filename, _ = download_file(
                                attachment['url'],
                                'subscribestar',
                                user_id,
                                str(post_id),
                                name = name
                            )
                            #add it to the list
                            post_model['attachments'].append({
                                'name': reported_filename,
                                'path': hash_filename
                            })

                    if docs_attachments:
                        for attachment in docs_attachments.children:
                            name = os.path.basename( urlparse(attachment.div.a['href']).path ) #gets the filename from the url
                            #download the file
                            reported_filename, hash_filename, = download_file(
                                attachment.div.a['href'],
                                'subscribestar',
                                user_id,
                                str(post_id),
                                name = name
                            )
                            #add it to the list
                            post_model['attachments'].append({
                                'name': reported_filename,
                                'path': hash_filename
                            })
                            
                    
                post_model['attachments'] = [json.dumps(attach) for attach in post_model['attachments']]

                #add the post to DB
                post_model['embed'] = json.dumps(post_model['embed'])
                post_model['file'] = json.dumps(post_model['file'])

                columns = post_model.keys()
                data = ['%s'] * len(post_model.values())
                data[-1] = '%s::jsonb[]' # attachments
                query = "INSERT INTO posts ({fields}) VALUES ({values}) ON CONFLICT (id, service) DO UPDATE SET {updates}".format(
                    fields = ','.join(columns),
                    values = ','.join(data),
                    updates = ','.join([f'{column}=EXCLUDED.{column}' for column in columns])
                )
                conn = get_raw_conn()
                try:
                    cursor3 = conn.cursor()
                    cursor3.execute(query, list(post_model.values()))
                    conn.commit()
                finally:
                    return_conn(conn)

                update_artist('subscribestar', user_id)
                delete_post_flags('subscribestar', user_id, str(post_id))

                if (config.ban_url):
                    requests.request('BAN', f"{config.ban_url}/{post_model['service']}/user/" + post_model['"user"'])
                delete_artist_cache_keys('subscribestar', user_id)

                log(import_id, f"Finished importing {post_id} from user {user_id}", to_client = False)


            except Exception:
                log(import_id, f"Error while importing {post_id} from user {user_id}", 'exception')
                continue
        
        more = soup.find("div", {"class": "posts-more"})
        
        if more: #we get the next HTML ready, and it'll process the new
            try:
                scraper = create_scrapper_session(useCloudscraper=True).get(
                    "https://www.subscribestar.com" + more['href'], #the next page
                    cookies=jar,
                    proxies=get_proxy()
                )
                scraper_data = scraper.json()['html']
                scraper.raise_for_status()
            except requests.HTTPError as exc:
                log(import_id, f'Status code {exc.response.status_code} when contacting SubscribeStar API.', 'exception')
                return
                
        else: #We got all the posts, exit
            log(import_id, f"Finished scanning for posts.")
            index_artists()
            return