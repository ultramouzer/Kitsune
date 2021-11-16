import json
import sys
from typing import List

from src.internals.utils.logger import log

from development.internals.database import query_db
from development.lib.randoms.types import Random_File
from development.types.models import File

sys.setrecursionlimit(100000)


def import_files(import_id: str, files: List[Random_File]):
    """Imports test files."""

    log(import_id, "Importing files...")
    log(import_id, f'{len(files)} files are going to be \"imported\"')

    for file in files:
        log(import_id, f"Importing file \"{file['path']}\"")
        # transform the file into `File_Model` there
        import_file(file)

    log(import_id, "Done importing file.")


def import_file(file: File):
    """Imports a single test file"""
    save_dm_to_db(file)


def save_dm_to_db(file: File):
    """Save test dm to DB"""
    query_params = dict(
    )

    query = """
    """
    query_db(query, query_params)
