import datetime
from typing import Optional, Protocol, Union


class CacheProtocol(Protocol):

    def get(self, key: str, default_value: Optional[str]) -> str:
        ...

    def set(self, key: str, value: str, time_to_live: Union[datetime.timedelta, float, int]) -> bool:
        ...
