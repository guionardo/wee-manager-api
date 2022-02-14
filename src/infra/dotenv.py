import logging
import os
from typing import Union


def load_dotenv(source: Union[str, dict] = '.env'):
    if isinstance(source, str):
        source = _read_file_env(source)
    log = logging.getLogger(__name__)
    if len(source) == 0:
        log.warning('No environment read from source %s', source)
        return
    os.environ.update(source)
    log.debug('Environment: %s', source)


def _read_file_env(filename: str) -> dict:
    """Read env file and returns a dict with key and values"""
    if not os.path.isfile(filename):
        raise FileNotFoundError(filename)
    source = {}
    with open(filename) as file:
        for line in file.readlines():
            line = line.strip().replace('\n', '').replace('\r', '')
            if line.startswith('#') or '=' not in line:
                continue
            key, value = line.split('=', 1)
            source[key] = value

    log = logging.getLogger(__name__)
    log.debug('Environment from file: %s = %s', filename, source)
    return source
