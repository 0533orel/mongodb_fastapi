import os
import unittest
from unittest.mock import patch
from urllib.parse import urlsplit, unquote_plus
from services.data_loader.config import mongo_uri
from services.data_loader import mongo_dal


class ConfigTests(unittest.TestCase):
    def test_missing_credentials_never_create_client(self):
        with patch.dict(os.environ, {}, clear=True), patch.object(mongo_dal, "AsyncIOMotorClient") as client:
            with self.assertRaisesRegex(ValueError, "Set MONGO_URI"):
                mongo_dal.get_client()
            client.assert_not_called()

    def test_explicit_local_uri(self):
        with patch.dict(os.environ, {"MONGO_URI": "mongodb://localhost:27017"}, clear=True):
            self.assertEqual(mongo_uri(), "mongodb://localhost:27017")

    def test_reserved_characters_are_encoded(self):
        value = "fixture" + ":/@?# value"
        with patch.dict(os.environ, {"MONGO_USER": "demo@example", "MONGO_PASS": value}, clear=True):
            uri = urlsplit(mongo_uri())
            self.assertEqual(unquote_plus(uri.password), value)
            self.assertEqual(unquote_plus(uri.username), "demo@example")
            self.assertEqual(uri.hostname, "mongodb")

    def test_blank_password_rejected(self):
        with patch.dict(os.environ, {"MONGO_USER": "demo", "MONGO_PASS": " "}, clear=True):
            with self.assertRaises(ValueError):
                mongo_uri()


class FixtureTests(unittest.IsolatedAsyncioTestCase):
    async def test_list_synthetic_people_without_database(self):
        from unittest.mock import MagicMock
        rows = [{"first_name": "Demo", "last_name": "Person"}]

        async def cursor():
            for row in rows:
                yield row

        collection = MagicMock()
        collection.find.return_value = cursor()
        with patch.object(mongo_dal, "get_collection", return_value=collection):
            self.assertEqual(await mongo_dal.list_people(), rows)
