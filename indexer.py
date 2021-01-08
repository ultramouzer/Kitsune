from psycopg2.extras import RealDictCursor
from bs4 import BeautifulSoup
from proxy import get_proxy
import cloudscraper
import requests
import psycopg2
import config
def index_artists():
    conn = psycopg2.connect(
        host = config.database_host,
        dbname = config.database_dbname,
        user = config.database_user,
        password = config.database_password,
        cursor_factory = RealDictCursor
    )
    cursor = conn.cursor()
    cursor.execute('select "user", "service" from "booru_posts" as "post" where not exists (select * from "lookup" where id = post.user) group by "user", "service"')
    results = cursor.fetchall()

    for post in results:
        if post.service == 'patreon':
            scraper = cloudscraper.create_scraper()
            user = scraper.get('https://www.patreon.com/api/user/' + id).json()
            model = {
                "id": post["user"],
                "name": user["data"]["attributes"]["vanity"] or user["data"]["attributes"]["full_name"],
                "service": "patreon"
            }
        elif post.service == 'fanbox':
            user = requests.get('https://api.fanbox.cc/creator.get?userId=' + id, headers={"origin":"https://fanbox.cc"}).json()
            model = {
                "id": post["user"],
                "name": user["body"]["creatorId"],
                "service": "fanbox"
            }
        elif post.service == 'gumroad':
            data = requests.get('https://gumroad.com/' + id).text
            soup = BeautifulSoup(data, 'html.parser')
            model = {
                "id": post["user"],
                "name": soup.find('h2', class_='creator-profile-card__name js-creator-name').string.replace("\n", ""),
                "service": "gumroad"
            }
        elif post.service == 'subscribestar':
            data = requests.get('https://subscribestar.adult/' + id).text
            soup = BeautifulSoup(data, 'html.parser')
            model = {
                "id": post["user"],
                "name": soup.find('div', class_='profile_main_info-name').string,
                "service": "subscribestar"
            }
        elif post.service == 'dlsite':
            data = requests.get('https://www.dlsite.com/eng/circle/profile/=/maker_id/' + id).text
            soup = BeautifulSoup(data, 'html.parser')
            model = {
                "id": post["user"],
                "name": soup.find('strong', class_='prof_maker_name').string,
                "service": "dlsite"
            }
        
        columns = model.keys()
        data = ['%s'] * len(model.values())
        query = "INSERT INTO booru_posts ({fields}) VALUES ({values})".format(
            fields = ','.join(columns),
            values = ','.join(data)
        )
        cursor.execute(query, model.values())
        conn.commit()

    conn.close()