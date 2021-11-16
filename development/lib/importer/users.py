from development.types.models import User
from typing import List
from src.internals.database.database import get_raw_conn, return_conn
from src.internals.utils.logger import log
# from .comments import import_comments


def import_users(import_id: str, users: List[User]):
    """Imports test users."""
    log(import_id, f"{len(users)} creators are going to be \"imported\"")

    while True:
        if users:
            for user in users:
                log(import_id, f"Importing user \"{user['id']}\"")
                import_user(import_id, user)
            log(import_id, "Finished importing users")
            return

        else:
            log(import_id, "User not supplied. Will not be imported.")
            return


def import_user(import_id: str, user: User):
    """Imports a test user."""

    # if is_artist_dnp('kemono-dev', user['id']):
    #     log(import_id, f"Skipping user {user['id']} because they are in do not post list")
    #     return

    try:
        save_user_to_db(user)
        log(import_id, f"Finished importing creator \"{user['id']}\"")
    except Exception as e:
        log(import_id, f"ERROR {e}: FAILED TO IMPORT USER \"{user['id']}\"")


def save_user_to_db(user: User):
    columns = user.keys()
    values = ['%s'] * len(user.values())
    query = """
        INSERT INTO lookup ({fields})
        VALUES ({values})
        ON CONFLICT (id, service)
            DO NOTHING
    """.format(
        fields=','.join(columns),
        values=','.join(values)
    )

    conn = get_raw_conn()
    try:
        cursor = conn.cursor()
        cursor.execute(query, list(user.values()))
        conn.commit()
    finally:
        return_conn(conn)
