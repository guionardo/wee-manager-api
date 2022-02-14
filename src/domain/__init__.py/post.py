"""Post

{
    "_id": 1,
    "post_id": 1,
    "user_id": 1,
    "page_id": null,
    "user_type": "user",
    "post_type": "video",
    "text": "Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.",
    "likes": -1,
    "comments": 3,
    "interacao": 1644249403,
    "posts_images": [],
    "posts_videos": [
        {
            "post_id": 1,
            "source": "video/2022/February/8628d11a12ca73d128e2133d1afd22c2-a0cc7a4f-4f25-47d0-a700-296663a7ffef.mp4",
            "bucket": "desenvolvimento",
            "url": "https://desenvolvimento.us-east-1.linodeobjects.com/uploads/video/2022/February/8628d11a12ca73d128e2133d1afd22c2-a0cc7a4f-4f25-47d0-a700-296663a7ffef.mp4"
        }
    ],
    "posts_links": [],
    "posts_medias": [],
    "posts_comments": [],
    "__v": 0,
    "user": {
        "user_id": 1,
        "user_name": "bomperfil",
        "user_verified": "1",
        "user_firstname": "Social",
        "user_lastname": "Wee",
        "user_gender": "male",
        "user_picture": "2022/January/0b831e91478c66f7b859935790925c4e-dfe6b9f7-c48b-4328-9f3f-4836be85dbd0.jpg",
        "user_privacidade": "publica",
        "get_avatar_url": "https://desenvolvimento.us-east-1.linodeobjects.com/uploads/avatar/2022/January/0b831e91478c66f7b859935790925c4e-dfe6b9f7-c48b-4328-9f3f-4836be85dbd0.jpg"
    },
    "page": null,
    "liked": true,
    "saved": true,
    "managed": false,
},
"""

from dataclasses import dataclass
from typing import List, Optional
from .post_video import PostVideo
from .user import User
from .page import Page


@dataclass
class Post:
    _id: int
    post_id: int
    user_id: int
    page_id: int
    user_type: str
    post_type: str
    text: str
    likes: int
    comments: int
    interacao: int
    posts_images: List[str]  # TODO: Verificar classe de imagem
    posts_videos: List[PostVideo]
    posts_links: List[str]   # TODO: Verificar classe de link
    posts_medias: List[str]  # TODO: Verificar classe de media
    user: User
    page: Page
    liked: Optional[bool]
    saved: Optional[bool]
    managed: Optional[bool]
