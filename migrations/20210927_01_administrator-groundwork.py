
"""
Add role column to accounts table, make index account_idx on accounts table, add notifications table with indexes
"""
from yoyo import step
__depends__ = {'20211003_01_vHxE2-create-auto-import-tables'}

steps = [
    step(
    "ALTER TABLE account ADD COLUMN  role varchar DEFAULT 'consumer';",

    "ALTER TABLE account DROP COLUMN role;"
    ),

    step(
        "CREATE INDEX IF NOT EXISTS account_idx ON account USING BTREE (username, created_at, role);",

    "DROP INDEX IF EXISTS account_idx;"
    ),

    step(
    """
    CREATE TABLE IF NOT EXISTS notifications (
        id BIGSERIAL PRIMARY KEY,
        account_id INT NOT NULL,
        type SMALLINT NOT NULL,
        extra_info jsonb,
        created_at TIMESTAMP WITHOUT TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
        is_seen BOOLEAN NOT NULL DEFAULT FALSE,
        FOREIGN KEY (account_id) REFERENCES account(id)
    );

    CREATE INDEX IF NOT EXISTS notifications_account_id_idx ON notifications USING BTREE ("account_id");
    CREATE INDEX IF NOT EXISTS notifications_created_at_idx ON notifications USING BTREE ("created_at");
    CREATE INDEX IF NOT EXISTS notifications_type_idx ON notifications USING BTREE ("type");
    """,

    """
    DROP TABLE IF EXISTS notifications;
    """
    )
]
