import logging
from dataclasses import asdict, is_dataclass
from typing import Any, Collection, Tuple

from src.data.engines import DataAccessConnection
from src.data.mongo_entity_counter_context import MongoEntityCounterContext
from src.infra.exceptions import MissingIdInModelException, StartupException
from src.protocols.crud_protocol import CrudProtocol


class MongoRepository(CrudProtocol):

    def __init__(self, dac: DataAccessConnection,
                 entity_name: str, entity_type: type) -> None:
        if not is_dataclass(entity_type):
            raise StartupException(
                'entity_type must be a dataclass', self.__class__)
        self._entity_name = entity_name
        self._entity_type = entity_type
        self._id_field_name = '_id'
        self.log = logging.getLogger(self.__class__.__name__)
        self._dac = dac
        super().__init__(dac)

    def _setup_model(self) -> Tuple[str, str, type]:
        return (self._entity_name, '_id', self._entity_type)

    def get_last_id(self):
        return self.collection.find()

    @property
    def collection(self) -> Collection:
        return self._dac.mongodb_database[self._entity_name]

    def get(self, data_id):
        return self.collection.find_one({self._id_field_name: data_id})

    def delete(self, data_id):
        return self.collection.find_one_and_delete({
            self._id_field_name: data_id
        })

    def insert(self, data) -> Any:
        as_dict = asdict(data)
        with MongoEntityCounterContext(self._dac, self._entity_name) as ctr:
            if not as_dict.get(self._id_field_name):
                as_dict[self._id_field_name] = ctr.last_id+1

            result = self.collection.insert_one(as_dict)
            ctr.set_last_inserted_id(result.inserted_id)
            return self._entity_type(**as_dict)

        return None

    def update(self, data):
        as_dict = asdict(data)
        data_id = as_dict.get(self._id_field_name, None)
        if not data_id:
            raise MissingIdInModelException(
                f'expected:{self._id_field_name}', data)
        result = self.collection.find_one_and_replace(
            {self._id_field_name: data_id}, as_dict)
        return result
