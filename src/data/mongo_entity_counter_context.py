import logging
import threading
from datetime import datetime

from src.data.engines import DataAccessConnection


class MongoEntityCounterContext:
    """Context class to control autoincrement id for mongodb colllections"""

    _lock = threading.Lock()

    def __init__(self, dac: DataAccessConnection, entity_name: str,
                 update_on_exit: bool = True):
        self._dac = dac
        self._entity_name = entity_name
        self._update_on_exit = update_on_exit
        self._last_inserted_id = None
        self._last_id = 0
        self.log = logging.getLogger(self.__class__.__name__)
        self._col = self._dac.mongodb_database.get_collection(
            '_entities_counter')

    @property
    def last_id(self) -> int:
        return self._last_id

    def __enter__(self):
        self._lock.acquire()
        self._last_inserted_id = None
        data_count = self._col.find_one({'_id': self._entity_name})
        self._last_id = 0 if not data_count else data_count.get('last_id', 0)

        return self

    def __exit__(self, exc_type, exc_value, exc_tc):
        if exc_type:
            self.log.error('Exception during MongoEntityCounterContext: %s',
                           str(exc_value),
                           exc_info=(exc_type, exc_value, exc_tc))
        else:
            if self._update_on_exit:
                last_id = self._last_inserted_id or self._last_id+1
                self._col.replace_one({'_id': self._entity_name},
                                      {
                    '_id': self._entity_name,
                    'last_id': last_id,
                    'operation_timestamp': datetime.utcnow()
                },
                    upsert=True)
        self._lock.release()

    def set_last_inserted_id(self, id: int):
        self._last_inserted_id = id
