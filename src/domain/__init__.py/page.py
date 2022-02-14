"""Page

{
    "page_id": 2,
    "page_admin": 1,
    "page_name": "f5e25dcbd326baa79f18158acf4a4c62",
    "page_title": "Brasil é lindo",
    "page_picture": "photos/2021/07/bomperfil_9c2c019488ff7041353f9404aa4e2f02_cropped.jpg",
    "get_avatar_url": null,
    "get_cover_url": null
}"""

from dataclasses import dataclass


@dataclass
class Page:
    page_id: int
    page_admin: int
    page_name: str
    page_title: str
    page_picture: str
    get_avatar_url: str
    get_cover_url: str
