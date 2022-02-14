import logging
import os
import tempfile
import unittest

from src.infra.dotenv import __name__ as dotenv_name
from src.infra.dotenv import _read_file_env, load_dotenv


class TestDotEnv(unittest.TestCase):

    SAMPLE = {'VAR1': '1234', 'VAR2': 'ABCD', 'VAR4': 'ZZZZ'}

    def test_read_file_env(self):
        with tempfile.NamedTemporaryFile('w', delete=True) as tmp:
            tmp.write(
                'VAR1=1234\nVAR2=ABCD\n#COMMENT=TEST\nVAR4=ZZZZ\n#ANOTHER COMMENT')
            tmp.flush()
            source = _read_file_env(tmp.name)

        self.assertEqual(3, len(source))
        self.assertDictEqual(
            {'VAR1': '1234', 'VAR2': 'ABCD', 'VAR4': 'ZZZZ'}, source)

    def test_load_env(self):
        with self.assertLogs(dotenv_name, level=logging.WARNING):
            load_dotenv({})

        envs = {'TEST1': 'ABCD', 'TEST2': '1234'}
        load_dotenv(envs)
        self.assertDictContainsSubset(envs, os.environ)
