"""
Add comment indexes
"""

from yoyo import step

__depends__ = {'20210614_01_YW8Os-add-comment-tables'}

steps = [
    step('CREATE INDEX comment_idx ON comments USING btree ("post_id")', 'DROP INDEX comment_idx')
]
