from src.internals.database.database import get_raw_conn, return_conn

from typing import List

def get_service_keys(amount: int) -> List[int]:
    conn = get_raw_conn()
    cursor = conn.cursor()
    args_dict = dict(
        amount= amount
    )
    query = """
        SELECT id
        FROM saved_session_keys
        LIMIT %(amount)s
    """
    cursor.execute(query, args_dict)
    keys = cursor.fetchall()
    conn.commit()
    return_conn(conn)
    return [key['id'] for key in keys] if keys else []

def kill_service_keys(key_ids: List[str]):
    conn = get_raw_conn()
    cursor = conn.cursor()
    args_dict = dict(
        key_ids= key_ids
    )
    query = """
        UPDATE saved_session_keys
        SET dead = TRUE
        WHERE id = ANY (%(key_ids)s)
    """
    cursor.execute(query, args_dict)
    conn.commit()
    return_conn(conn)
    return True
