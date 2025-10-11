from typing import TypedDict


class Context(TypedDict):
    access_token: str
    user_id: str
    first_name: str


class Metadata(TypedDict):
    date: str
    timezone: str
