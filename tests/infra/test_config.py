import unittest

from src.infra.config import Configuration


class TestConfiguration(unittest.TestCase):

    def test_empty_configuration(self):
        with self.assertRaises(EnvironmentError):
            Configuration({})

    def test_configuration(self):
        c = Configuration(dict(
            MYSQL_CONNECTION_STRING='mysql',
            MONGODB_CONNECTION_STRING='mongo'
        ))
        self.assertEqual('mysql', c.MYSQL_CONNECTION_STRING)
        self.assertEqual('mongo', c.MONGODB_CONNECTION_STRING)
