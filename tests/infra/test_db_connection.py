import unittest
from dataclasses import dataclass
from datetime import datetime
from typing import Optional


from src.data.engines import DataAccessConnection
from src.data.mongo_repository import MongoRepository
from src.infra.config import Configuration
from src.infra.dotenv import load_dotenv


@dataclass
class TestModel:
    _id: Optional[int]
    name: str
    birth_date: datetime
    active: bool
    creation_date: datetime = datetime.utcnow()


class MongoTestRepository(MongoRepository):

    def __init__(self, dac: DataAccessConnection) -> None:
        super().__init__(dac, 'test', TestModel)


class TestDbConnection(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        load_dotenv()
        cls.conf = Configuration()
        cls.dac = DataAccessConnection(cls.conf)
        return super().setUpClass()

    def test_connections(self):
        self.assertIsNotNone(self.dac)

    def test_mongodb_testing_collection(self):
        repo = MongoTestRepository(self.dac)
        data = TestModel(_id=0, name='Guionardo', birth_date=datetime(
            1977, 2, 5), active=True)
        inserted_data = repo.insert(data)
        print(inserted_data)

        inserted_data.active = False
        data2 = repo.update(inserted_data)

        # repo.delete(inserted_id)
