from typing import Any, Protocol, Tuple
from src.data.engines import DataAccessConnection


class CrudProtocol(Protocol):

    _entity_name: str
    _id_field_name: str
    _entity_type: type
    _dac: DataAccessConnection

    def __init__(self, dac: DataAccessConnection) -> None:
        super().__init__()
        self._entity_name, self._id_field_name = self._setup_model()
        self._dac = dac

    def _setup_model(self) -> Tuple[str, str, type]:
        """Returns a tuple with:
        entity name (str)
        id field name (str)
        type of entity"""

    def get(self, id):
        """Returns data or None if not found"""

    def delete(self, id):
        """Delete data throwing Exception if error"""

    def insert(self, data) -> Any:
        """Inserts data, returning id or throwing exception if error"""

    def update(self, data):
        """Updates data, throwing Exception if error"""
