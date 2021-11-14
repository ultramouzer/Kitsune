import json
import sys
from typing import List

from src.internals.utils.logger import log

from development.internals.database import query_db
from development.types.models import DM

sys.setrecursionlimit(100000)


def import_dms(import_id: str, dms: List[DM]):
    """Imports test DMs."""

    log(import_id, "Importing DMs...")

    while True:
        for dm in dms:
            log(import_id, f"Importing dm \"{dm['id']}\" from user \"{dm['user']}\"")
            import_dm(dm)

        log(import_id, "Done importing DMs.")
        return


def import_dm(dm: DM):
    """Imports a single test DM"""
    save_dm_to_db(dm)


def save_dm_to_db(dm: DM):
    """Save test dm to DB"""
    query_params = dict(
        import_id=dm['import_id'],
        contributor_id=dm['contributor_id'],
        id=dm['id'],
        user=dm['user'],
        service=dm['service'],
        file=json.dumps(dm['file']),
        published=dm['published'],
        content=dm['content']
    )

    query = """
        INSERT INTO unapproved_dms
            (import_id, contributor_id, id, \"user\", service, file, published, content)
        VALUES
            (%(import_id)s, %(contributor_id)s, %(id)s, %(user)s, %(service)s, %(file)s, %(published)s, %(content)s)
        ON CONFLICT (id, service)
            DO NOTHING
    """
    query_db(query, query_params)
