import time
import shutil
import tempfile
import subprocess
import os

import pymongo


class MongoTemporaryInstance():
    def __init__(self, mongdb_host='localhost', mongodb_port=52010):
        self._tmpdir = tempfile.mkdtemp()
        self._mongodb_port = mongodb_port
        self._mongodb_host = mongdb_host

    def start_mongodb(self):
        self._process = subprocess.Popen(['mongod', '--bind_ip', self._mongodb_host,
                                          '--port', str(self._mongodb_port),
                                          '--dbpath', self._tmpdir,
                                          '--nojournal', '--nohttpinterface',
                                          '--noauth', '--smallfiles',
                                          '--syncdelay', '0',
                                          '--maxConns', '10',
                                          '--nssize', '1', ],
                                         stdout=open(os.devnull, 'wb'),
                                         stderr=subprocess.STDOUT)

        # XXX: wait for the instance to be ready
        #      Mongo is ready in a glance, we just wait to be able to open a
        #      Connection.
        for i in range(3):
            time.sleep(0.1)
            try:
                print i
                self._conn = pymongo.MongoClient('localhost', self._mongodb_port)
            except pymongo.errors.ConnectionFailure:
                continue
            else:
                break
        else:
            self.shutdown()
            assert False, 'Cannot connect to the mongodb test instance'
        print 'DONE'

    def mongo_create_db(self, db, collection, data):
        test_db = self._conn[db]
        self._collection = test_db[collection]
        self.mongo_inser_data(data)

    def mongo_drop_database(self, db):
        self._conn.drop_database(db)

    def mongo_inser_data(self, data):
        self._collection.insert(data)

    def mongo_database_names(self, db):
        return self._conn.database_names()

    def shutdown(self):
        if self._process:
            self._process.terminate()
            self._process.wait()
            self._process = None
            shutil.rmtree(self._tmpdir, ignore_errors=True)

"""
if __name__ == '__main__':
    db = MongoTemporaryInstance()
    db.start_mongodb()

    data = {"firstName": "John", "lastName": "Smith", "age": 25}
    db.mongo_create_db('goo', 'data')
    db.mongo_inser_data(data)

    db.shutdown()

"""
