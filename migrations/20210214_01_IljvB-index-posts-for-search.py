"""
Index posts for search
"""

from yoyo import step

__depends__ = {'20210120_01_PZzeb-apply-primary-key-constraint-to-lookup-table'}

steps = [
    step(
        "CREATE INDEX IF NOT EXISTS search_idx ON posts USING GIN (to_tsvector('english', content || ' ' || title))",
        "DROP INDEX search_idx"
    )
]
