"""PostComment

 {
    "comment_id": 11,
    "user_id": 49,
    "text": "Oi",
    "time": "2022-02-10T00:06:27.000Z",
    "likes": 0,
    "replies": 0,
    "user": {
        "user_id": 49,
        "user_name": "joãob9f897aa",
        "user_verified": "0",
        "user_firstname": "João ",
        "user_lastname": "Neto",
        "user_gender": "male",
        "user_picture": "2022/February/bfea37cc0ffb86c7b9c5ee5c6f173b75-3fcb09ef-02d9-404d-a27f-c66eba30689c.jpg",
        "user_privacidade": "publica",
        "get_cover_url": null
    },
    "page": null,
    "liked": false
},
"""
from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from .page import Page
from .user import User


@dataclass
class PostComment:
    comment_id: int
    user_id: 49
    text: str
    time: datetime
    likes: int
    replies: int
    user: Optional[User]
    page: Optional[Page]
    liked: bool
