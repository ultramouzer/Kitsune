from psycopg2.extensions import connection

from src.internals.database.database import get_raw_conn, return_conn

from typing import List
from development.types.models import Database_Model, Query_Args


def save_several_models_to_db(models: List[Database_Model]):
    """
    Saves several instances of a model to a database.
    """
    if len(models) == 1:
        save_model_to_db(models[0])
    else:
        query_args = Query_Args()
        query = """"""
        query_db(query, query_args)


def save_model_to_db(model: Database_Model):
    """
    Saves an instance of a model to a database.
    """
    query_args = Query_Args(
        keys=model.keys(),
        values=model.values()
    )
    query = """"""

    return query_db(query, query_args)


def query_db(query: str, query_args: Query_Args):
    """
    Performs an operation on a database.
    """
    conn = get_raw_conn()
    try:
        cursor = conn.cursor()
        cursor.execute(query, query_args)
        conn.commit()
    finally:
        return_conn(conn)


def query_db_without_commit(conn: connection, query: str, query_args: Query_Args):
    """
    Performs an operation on a database without committing the result.
    """
    cursor = conn.cursor()
    cursor.execute(query, query_args)
