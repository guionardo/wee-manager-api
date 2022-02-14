from pymongo import MongoClient
from pymongo.database import Database
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from src.infra.config import Configuration
from src.infra.exceptions import StartupException


class DataAccessConnection:

    def __init__(self, config: Configuration) -> None:
        self._config = config
        self._mysql_engine: Engine = create_engine(
            config.MYSQL_CONNECTION_STRING)
        self._mongodb_client: MongoClient = MongoClient(
            config.MONGODB_CONNECTION_STRING)
        try:
            mdb = self._mongodb_client.get_default_database()
            self._mongodb_database = mdb
        except Exception as exc:
            raise StartupException(
                'Missing default database in MONGODB_CONNECTION_STRING', exc)

    @property
    def mysql_engine(self) -> Engine:
        return self._mysql_engine

    @property
    def mongodb_client(self) -> MongoClient:
        return self._mongodb_client

    @property
    def mongodb_database(self) -> Database:
        return self._mongodb_database
