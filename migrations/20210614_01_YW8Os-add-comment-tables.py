"""
Add comment tables
"""

from yoyo import step

__depends__ = {'20210611_01_jpGYN-add-update-index'}

steps = [
    step(
        """
            CREATE TABLE IF NOT EXISTS comments (
                "id" varchar(255) NOT NULL,
                "post_id" varchar(255) NOT NULL,
                "parent_id" varchar(255),
                "commenter" varchar(255) NOT NULL,
                "service" varchar(20) NOT NULL,
                "content" text NOT NULL DEFAULT '',
                "added" timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
                "published" timestamp,
                PRIMARY KEY (id, service)
            );
        """
    )
]
