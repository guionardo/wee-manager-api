"""Post Video

{
    "post_id": 1,
    "source": "video/2022/February/8628d11a12ca73d128e2133d1afd22c2-a0cc7a4f-4f25-47d0-a700-296663a7ffef.mp4",
    "bucket": "desenvolvimento",
    "url": "https://desenvolvimento.us-east-1.linodeobjects.com/uploads/video/2022/February/8628d11a12ca73d128e2133d1afd22c2-a0cc7a4f-4f25-47d0-a700-296663a7ffef.mp4"
}
"""
from dataclasses import dataclass


@dataclass
class PostVideo:
    post_id: int
    source: str
    bucket: str
    url: str
