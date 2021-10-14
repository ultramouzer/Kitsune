from development.internals import dev_random, service_name

from development.types import Service_Key_DB

def service_key(account_id: str):
    key_item = Service_Key_DB(
        service= service_name,
        key= dev_random.text(),
        contributor_id= account_id,
    )
    return key_item
