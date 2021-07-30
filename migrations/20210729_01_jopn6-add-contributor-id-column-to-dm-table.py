"""
Add contributor ID column to DM table
"""

from yoyo import step

__depends__ = {'20210707_04_l1vte-add-dm-indexes'}

steps = [
    step(
        "ALTER TABLE unapproved_dms ADD COLUMN contributor_id varchar(255)",
        "ALTER TABLE unapproved_dms DROP COLUMN contributor_id"
    )
]
