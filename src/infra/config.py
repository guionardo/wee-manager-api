from .base_config import BaseConfiguration


class Configuration(BaseConfiguration):

    __slots__ = ['MYSQL_CONNECTION_STRING',
                 'MONGODB_CONNECTION_STRING']

    MYSQL_CONNECTION_STRING: str
    MONGODB_CONNECTION_STRING: str
    DEBUG: bool = False
