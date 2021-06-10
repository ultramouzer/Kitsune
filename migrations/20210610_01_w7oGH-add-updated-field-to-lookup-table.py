"""
Add updated field to lookup table
"""

from yoyo import step
from psycopg2.extras import RealDictCursor

__depends__ = {'20210529_01_LO1OU-add-primary-keys-to-discord-posts'}

def apply_step(conn):
    cursor1 = conn.cursor()
    cursor1.execute("ALTER TABLE lookup ADD COLUMN updated timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP")
    cursor2 = conn.cursor(cursor_factory=RealDictCursor)
    cursor2.execute("SELECT * FROM lookup")
    artists = cursor2.fetchall()
    for artist in artists:
        cursor3 = conn.cursor()
        cursor3.execute('SELECT max(added) as max FROM posts WHERE service = %s AND "user" = %s', (artist['service'], artist['id']))
        last_updated = cursor3.fetchone()[0]
        cursor4 = conn.cursor()
        cursor4.execute('UPDATE lookup SET updated = %s WHERE service = %s AND id = %s', (last_updated, artist['service'], artist['id']))

steps = [
    step(
        apply_step,
        "ALTER TABLE lookup DROP COLUMN updated"
    )
]