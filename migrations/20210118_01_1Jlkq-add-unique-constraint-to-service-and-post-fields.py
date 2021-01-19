"""
Add unique constraint to service and post fields
"""

from yoyo import step

__depends__ = {"initial"}

steps = [
    step(
        "ALTER TABLE booru_posts ADD CONSTRAINT posts_pk PRIMARY KEY (id, service) ON CONFLICT DO NOTHING"
        "ALTER TABLE booru_posts DROP CONSTRAINT posts_pk"
    )
]
