import sys
import json

from src.internals.utils.logger import log
from development.internals import service_name
from development.internals.database import query_db

from typing import List
from development.types.models import Post
sys.setrecursionlimit(100000)


def import_posts(import_id: str, posts: List[Post]):
    """Imports test posts."""

    log(import_id, f'{len(posts)} posts are going to be \"imported\".')

    while True:
        for post in posts:
            log(import_id, f"Importing post \"{post['id']}\" from user \"{post['user']}\".")
            import_post(post)

        log(import_id, "Done importing posts.")
        return


def import_post(post: Post):
    """
    Imports a single test post.
    """
    save_post_to_db(post)


def save_post_to_db(post: Post):
    """
    Saves test posts to DB.
    TODO: rewrite into more generic way.
    """
    query_params = dict(
        id=post['id'],
        user=post['user'],
        service=post['service'],
        file=json.dumps(post['file']),
        attachments=[json.dumps(attachment) for attachment in post['attachments']],
        published=post['published'],
        edited=post['edited'],
        title=post['title'],
        content=post['content']
    )

    query = """
        INSERT INTO posts
            (id, \"user\", service, file, attachments, published, edited, title, content)
        VALUES (%(id)s, %(user)s, %(service)s, %(file)s, %(attachments)s::jsonb[], %(published)s, %(edited)s, %(title)s, %(content)s)
        ON CONFLICT (id, service)
            DO NOTHING
    """
    query_db(query, query_params)
