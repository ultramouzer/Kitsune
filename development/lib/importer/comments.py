from typing import List
from development.types.models import Comment
from development.internals.database import query_db
from src.internals.utils.logger import log


def import_comments(import_id: str, comments: List[Comment]):
    """Imports test comments."""

    log(import_id, "Importing comments...")

    while True:
        for comment in comments:
            import_comment(comment)

        log(import_id, "Done importing comments.")
        return


def import_comment(comment: Comment):
    """Imports a single test comment."""
    save_comment_to_db(comment)


def save_comment_to_db(comment: Comment):
    """Save test dm to DB"""
    query_params = dict(
        id=comment['id'],
        post_id=comment['post_id'],
        parent_id=comment['parent_id'],
        commenter=comment['commenter'],
        service=comment['service'],
        content=comment['content'],
        published=comment['published']
    )
    query = """
        INSERT INTO comments
            (id, post_id, parent_id, commenter, service, content, published)
        VALUES
            (%(id)s, %(post_id)s, %(parent_id)s, %(commenter)s, %(service)s, %(content)s, %(published)s)
        ON CONFLICT (id, service)
            DO NOTHING
    """
    query_db(query, query_params)
