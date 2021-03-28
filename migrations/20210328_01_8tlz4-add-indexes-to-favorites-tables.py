"""
Add indexes to favorites tables
"""

from yoyo import step

__depends__ = {'20210322_01_In37S-add-account-field'}

steps = [
    step("""
        CREATE INDEX ON account_artist_favorite (service, artist_id)
    """),
    step("""
        CREATE INDEX ON account_post_favorite (service, artist_id, post_id)
    """)
]
