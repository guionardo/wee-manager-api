"""User

{
    "user_id": 1,
    "user_name": "bomperfil",
    "user_verified": "1",
    "user_firstname": "Social",
    "user_lastname": "Wee",
    "user_gender": "male",
    "user_picture": "2022/January/0b831e91478c66f7b859935790925c4e-dfe6b9f7-c48b-4328-9f3f-4836be85dbd0.jpg",
    "user_privacidade": "publica",
    "get_avatar_url": "https://desenvolvimento.us-east-1.linodeobjects.com/uploads/avatar/2022/January/0b831e91478c66f7b859935790925c4e-dfe6b9f7-c48b-4328-9f3f-4836be85dbd0.jpg"
}
"""
from dataclasses import dataclass


@dataclass
class User:
    user_id: int
    user_name: str
    user_verified: int
    user_firstname: str
    user_lastname: str
    user_gender: str
    user_picture: str
    user_privacidade: str
    get_avatar_url: str
