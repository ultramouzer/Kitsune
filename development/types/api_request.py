from typing import TypedDict

class API_Request(TypedDict):
    service: str
    session_key: str
    channel_ids: str
    save_session_key: str
    save_dms: str
    contributor_id: str
