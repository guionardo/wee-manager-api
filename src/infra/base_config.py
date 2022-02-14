import inspect
import os
import warnings


class BaseConfiguration:

    def __init__(self, source: dict = os.environ):
        fields_data = self._get_fields()
        self._set_fields(fields_data, source)

    def _get_fields(self) -> dict:
        members = inspect.getmembers(self)
        annotations = [m[1] for m in members if m[0] == '__annotations__'][0]
        slots = [m[1] for m in members if m[0] == '__slots__'][0]
        fields = {m[0]: m[1]
                  for m in members if m[0].isupper() and not callable(m[1])}
        field_names = set([a for a in annotations]+[f for f in fields])
        for field_name in field_names:
            if field_name not in slots:
                warnings.warn(
                    f'Missing declaration of field "{field_name}" in __slots__ of {self.__class__.__name__} class',
                    SyntaxWarning,
                    stacklevel=0,)
        for field_name in fields:
            if field_name not in annotations:
                warnings.warn(f'Missing type declaration of field "{field_name}" in {self.__class__.__name__} class',
                              SyntaxWarning)

        field_data = {}
        for field_name, field_type in annotations.items():
            field_data[field_name] = [field_type, None]
        for field_name, field_value in fields.items():
            if not field_data.get(field_name):
                field_data[field_name] = [type(field_value), field_value]
            else:
                field_data[field_name][1] = field_value

        return field_data

    def _set_fields(self, field_data: dict, source: dict):
        for field_name, (field_type, field_value) in field_data.items():
            source_value = source.get(field_name)
            if source_value is None:
                if field_value is None:
                    raise EnvironmentError('REQUIRED ENV', field_name)
                source_value = field_value
            setattr(self, field_name, field_type(source_value))
