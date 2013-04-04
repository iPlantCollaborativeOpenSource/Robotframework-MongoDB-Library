import pymongo
import subprocess
import tempfile
import shutil
import unittest
import os
import time
import sys

# Get src directory and put it in path
# To get import forking for MongoDBLibrary

ROOT_DIR = os.path.dirname(os.path.abspath('..'))
SRC_DIR = os.path.join(ROOT_DIR, "src")
sys.path.insert(0, SRC_DIR)

# Suppress logging from MongoDBLibrary
#f = open(os.devnull, 'w')
#sys.stdout = f

# settings for unit test
test_mongo_connection_host = 'localhost'
test_mongo_connection_port = 51000
test_database_name = 'test_database'
test_collection_name = 'test_collection'
data1 = {"firstName": "John","lastName": "Smith","age": 25,"address": {"streetAddress": "21 2nd Street","city": "New York","state": "NY","postalCode": 10021},"phoneNumbers": [{"type": "home","number": "212 555-1234"},{"type": "fax","number": "646 555-4567"}]}

from MongoDBLibrary import MongoDBLibrary


class TestMongoDBLibrary(unittest.TestCase):

    def setUp(self):
        self._tmpdir = tempfile.mkdtemp()
        self._process = subprocess.Popen(['mongod', '--bind_ip', test_mongo_connection_host,
                                          '--port', str(test_mongo_connection_port),
                                          '--dbpath', self._tmpdir,
                                          '--nojournal', '--nohttpinterface',
                                          '--noauth', '--smallfiles',
                                          '--syncdelay', '0',
                                          '--maxConns', '10',
                                          '--nssize', '1', ],
                                        stdout=open(os.devnull, 'wb'),
                                        stderr=subprocess.STDOUT)
        # Mongo is super fast but
        # Wait for database connection
        for i in range(5):
            time.sleep(0.1)
            try:
                self._conn = pymongo.MongoClient(test_mongo_connection_host, test_mongo_connection_port)
            except pymongo.errors.ConnectionFailure:
                continue
            else:
                break
        else:
            self.tearDown()
            assert False, 'Cannot connect to the mongodb test instance'

    def test_get_mongodb_databases(self):
        self.mongo_create_db()
        self.mongo_inser_data(data1)

        a = MongoDBLibrary()
        a.connect_to_mongodb(dbHost=test_mongo_connection_host, dbPort=test_mongo_connection_port)
        db = a.get_mongodb_databases()
        a.disconnect_from_mongodb()

        self.mongo_drop_database()

        expected = ['test_database', 'local']
        self.assertEqual(db, expected)

    def test_get_mongodb_collections(self):
        self.mongo_create_db()
        self.mongo_inser_data(data1)

        a = MongoDBLibrary()
        a.connect_to_mongodb(dbHost=test_mongo_connection_host, dbPort=test_mongo_connection_port)
        collection_names = a.get_mongodb_collections(test_database_name)
        a.disconnect_from_mongodb()

        self.mongo_drop_database()

        expected = ['system.indexes', 'test_collection']
        self.assertEqual(collection_names, expected)

    def test_drop_mongodb_database(self):
        self.mongo_create_db()
        self.mongo_inser_data(data1)

        a = MongoDBLibrary()
        a.connect_to_mongodb(dbHost=test_mongo_connection_host, dbPort=test_mongo_connection_port)
        a.drop_mongodb_database(test_database_name)
        a.disconnect_from_mongodb()

        database_names = self.mongo_database_names()
        expected = ['local']
        self.assertEqual(database_names, expected)

    def tearDown(self):
        # Terminate Mongodb process
        if self._process:
            self._process.terminate()
            self._process.wait()
            self._process = None
            shutil.rmtree(self._tmpdir, ignore_errors=True)

    def mongo_create_db(self, db=test_database_name, collection=test_collection_name):
        test_db = self._conn[db]
        self._collection = test_db[collection]

    def mongo_drop_database(self, db=test_database_name):
        self._conn.drop_database(db)

    def mongo_inser_data(self, data):
        self._collection.insert(data)

    def mongo_database_names(self, db=test_database_name, collection=test_collection_name):
        return self._conn.database_names()


if __name__ == '__main__':
    unittest.main()
