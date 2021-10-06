import sys
sys.path.append('./PixivUtil2')
sys.setrecursionlimit(100000)

from os import makedirs
from os.path import join
import requests
import datetime
import config
import json

from flask import current_app

from PixivUtil2.PixivModelFanbox import FanboxArtist, FanboxPost

from ..internals.database.database import get_conn, get_raw_conn, return_conn
from ..lib.artist import index_artists, is_artist_dnp, update_artist, delete_artist_cache_keys, delete_comment_cache_keys
from ..lib.post import post_flagged, post_exists, delete_post_flags, move_to_backup, delete_backup, restore_from_backup, comment_exists
from ..lib.autoimport import encrypt_and_save_session_for_auto_import, kill_key
from ..internals.utils.proxy import get_proxy
from ..internals.utils.download import download_file, DownloaderException
from ..internals.utils.utils import get_import_id
from ..internals.utils.logger import log
from ..internals.utils.scrapper import create_scrapper_session

def import_comment(comment, user_id, post_id, import_id):
    commenter_id = comment['user']['userId']
    comment_id = comment['id']
    
    if comment_exists('fanbox', commenter_id, comment_id):
        log(import_id, f"Skipping comment {comment_id} from post {post_id} because already exists", to_client = False)
        return
    
    log(import_id, f"Starting comment import: {comment_id} from post {post_id}", to_client = False)

    post_model = {
        'id': comment_id,
        'post_id': post_id,
        'parent_id': comment['parentCommentId'] if comment['parentCommentId'] != '0' else None,
        'commenter': commenter_id,
        'service': 'fanbox',
        'content': comment['body'],
        'added': datetime.datetime.now(),
        'published': comment['createdDatetime'],
    }

    columns = post_model.keys()
    data = ['%s'] * len(post_model.values())
    query = "INSERT INTO comments ({fields}) VALUES ({values})".format(
        fields = ','.join(columns),
        values = ','.join(data)
    )
    conn = get_raw_conn()
    try:
        cursor = conn.cursor()
        cursor.execute(query, list(post_model.values()))
        conn.commit()
    finally:
        return_conn(conn)

    if comment.get('replies'):
        for comment in comment['replies']:
            import_comment(comment, user_id, post_id, import_id)
    
    if (config.ban_url):
        requests.request('BAN', f"{config.ban_url}/{post_model['service']}/user/" + user_id + '/post/' + post_model['post_id'])
    delete_comment_cache_keys(post_model['service'], user_id, post_model['post_id'])

def import_comments(key, post_id, user_id, import_id, url = None):
    if not url:
        url = f'https://api.fanbox.cc/post.listComments?postId={post_id}&limit=10'
    
    try:
        scraper = create_scrapper_session(useCloudscraper=False).get(
            url,
            cookies = { 'FANBOXSESSID': key },
            headers={ 'origin': 'https://fanbox.cc' },
            proxies=get_proxy()
        )
        scraper_data = scraper.json()
        scraper.raise_for_status()
    except requests.HTTPError:
        log(import_id, f'HTTP error when contacting Fanbox API ({url}). No comments will be imported.', 'exception')
        return
    
    if scraper_data.get('body'):
        for comment in scraper_data['body']['items']:
            comment_id = comment['id']
            try:
                import_comment(comment, user_id, post_id, import_id)
            except Exception as e:
                log(import_id, f"Error while importing comment {comment_id} from post {post_id}", 'exception', True)
                continue
    
    next_url = scraper_data['body'].get('nextUrl')
    if next_url:
        log(import_id, f"Processing next page of comments for post {post_id}", to_client = False)
        import_comments(key, post_id, user_id, import_id, url = next_url)

def import_posts(import_id, key, contributor_id = None, allowed_to_auto_import = None, key_id = None, url = 'https://api.fanbox.cc/post.listSupporting?limit=50'):
    try:
        scraper = create_scrapper_session(useCloudscraper=False).get(
            url,
            cookies={ 'FANBOXSESSID': key },
            headers={ 'origin': 'https://fanbox.cc' },
            proxies=get_proxy()
        )
        scraper_data = scraper.json()
        scraper.raise_for_status()
    except requests.HTTPError as exc:
        log(import_id, f'HTTP error when contacting Fanbox API ({url}). Stopping import.', 'exception')
        if (exc.response.status_code == 401 and key_id):
            kill_key(key_id)
        return

    if (allowed_to_auto_import and url == 'https://api.fanbox.cc/post.listSupporting?limit=50'):
        try:
            encrypt_and_save_session_for_auto_import('fanbox', key, contributor_id = contributor_id)
            log(import_id, f"Your key was successfully enrolled in auto-import!", to_client = True)
        except:
            log(import_id, f"An error occured while saving your key for auto-import.", 'exception')
    
    user_id = None
    if scraper_data.get('body'):
        for post in scraper_data['body']['items']:
            user_id = post['user']['userId']
            post_id = post['id']

            parsed_post = FanboxPost(post_id, None, post)
            if parsed_post.is_restricted:
                log(import_id, f'Skipping post {post_id} from user {user_id} because post is from higher subscription tier')
                continue
            try:
                if is_artist_dnp('fanbox', user_id):
                    log(import_id, f"Skipping post {post_id} from user {user_id} is in do not post list")
                    continue

                import_comments(key, post_id, user_id, import_id)

                if post_exists('fanbox', user_id, post_id) and not post_flagged('fanbox', user_id, post_id):
                    log(import_id, f'Skipping post {post_id} from user {user_id} because already exists')
                    continue

                log(import_id, f"Starting import: {post_id} from user {user_id}")

                post_model = {
                    'id': post_id,
                    '"user"': user_id,
                    'service': 'fanbox',
                    'title': post['title'],
                    'content': parsed_post.body_text,
                    'embed': {},
                    'shared_file': False,
                    'added': datetime.datetime.now(),
                    'published': post['publishedDatetime'],
                    'edited': post['updatedDatetime'],
                    'file': {},
                    'attachments': []
                }

                for i in range(len(parsed_post.embeddedFiles)):
                    if type(parsed_post.embeddedFiles[i]) is dict:
                        if parsed_post.embeddedFiles[i]['serviceProvider'] == 'twitter':
                            post_model['content'] += f"""
                                <a href="https://twitter.com/_/status/{parsed_post.embeddedFiles[i]['contentId']}" target="_blank">
                                    <div class="embed-view">
                                      <h3 class="subtitle">(Twitter)</h3>
                                    </div>
                                </a>
                                <br>
                            """
                        elif parsed_post.embeddedFiles[i]['serviceProvider'] == 'youtube': 
                            post_model['content'] += f"""
                                <a href="https://www.youtube.com/watch?v={parsed_post.embeddedFiles[i]['contentId']}" target="_blank">
                                    <div class="embed-view">
                                      <h3 class="subtitle">(YouTube)</h3>
                                    </div>
                                </a>
                                <br>
                            """
                        elif parsed_post.embeddedFiles[i]['serviceProvider'] == 'fanbox': 
                            post_model['content'] += f"""
                                <a href="https://www.pixiv.net/fanbox/{parsed_post.embeddedFiles[i]['contentId']}" target="_blank">
                                    <div class="embed-view">
                                      <h3 class="subtitle">(Fanbox)</h3>
                                    </div>
                                </a>
                                <br>
                            """
                        elif parsed_post.embeddedFiles[i]['serviceProvider'] == 'vimeo': 
                            post_model['content'] += f"""
                                <a href="https://vimeo.com/{parsed_post.embeddedFiles[i]['contentId']}" target="_blank">
                                    <div class="embed-view">
                                      <h3 class="subtitle">(Vimeo)</h3>
                                    </div>
                                </a>
                                <br>
                            """
                        elif parsed_post.embeddedFiles[i]['serviceProvider'] == 'google_forms': 
                            post_model['content'] += f"""
                                <a href="https://docs.google.com/forms/d/e/{parsed_post.embeddedFiles[i]['contentId']}" target="_blank">
                                    <div class="embed-view">
                                      <h3 class="subtitle">(Google Forms)</h3>
                                    </div>
                                </a>
                                <br>
                            """
                        elif parsed_post.embeddedFiles[i]['serviceProvider'] == 'soundcloud': 
                            post_model['content'] += f"""
                                <a href="https://soundcloud.com/{parsed_post.embeddedFiles[i]['contentId']}" target="_blank">
                                    <div class="embed-view">
                                      <h3 class="subtitle">(Soundcloud)</h3>
                                    </div>
                                </a>
                                <br>
                            """
                    elif type(parsed_post.embeddedFiles[i]) is str:
                        if i == 0:
                            reported_filename, hash_filename, _ = download_file(
                                parsed_post.embeddedFiles[i],
                                'fanbox',
                                user_id,
                                post_id,
                                cookies={ 'FANBOXSESSID': key },
                                headers={ 'origin': 'https://fanbox.cc' }
                            )
                            post_model['file']['name'] = reported_filename
                            post_model['file']['path'] = hash_filename
                        else:
                            reported_filename, hash_filename, _ = download_file(
                                parsed_post.embeddedFiles[i],
                                'fanbox',
                                user_id,
                                post_id,
                                cookies={ 'FANBOXSESSID': key },
                                headers={ 'origin': 'https://fanbox.cc' }
                            )
                            post_model['attachments'].append({
                                'name': reported_filename,
                                'path': hash_filename
                            })

                post_model['embed'] = json.dumps(post_model['embed'])
                post_model['file'] = json.dumps(post_model['file'])
                for i in range(len(post_model['attachments'])):
                    post_model['attachments'][i] = json.dumps(post_model['attachments'][i])

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
                    cursor = conn.cursor()
                    cursor.execute(query, list(post_model.values()))
                    conn.commit()
                finally:
                    return_conn(conn)

                update_artist('fanbox', user_id)
                delete_post_flags('fanbox', user_id, post_id)

                if (config.ban_url):
                    requests.request('BAN', f"{config.ban_url}/{post_model['service']}/user/" + post_model['"user"'])
                delete_artist_cache_keys('fanbox', user_id)

                log(import_id, f'Finished importing {post_id} for user {user_id}', to_client = False)
            except Exception as e:
                log(import_id, f'Error importing post {post_id} from user {user_id}', 'exception')
                continue
        
        next_url = scraper_data['body'].get('nextUrl')
        if next_url:
            log(import_id, f'Finished processing page ({url}). Processing {next_url}')
            import_posts(import_id, key, url = next_url)
        else:
            log(import_id, f'Finished scanning for posts')
            index_artists()
    else:
        log(import_id, f'No posts detected.')