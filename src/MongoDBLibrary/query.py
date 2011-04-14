#  Copyright (c) 2011 Jerry Schneider
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

import json
from pymongo.objectid import ObjectId

class Query(object):
    """
    Query handles all the querying done by the Database Library. 
    """

    def get_mongodb_databases(self):
        """
        Returns a list of all of the databases currently on the MongoDB 
        server you are connected to.

        Usage is:
        | @{allDBs} | Get Mongodb Databases |
        | Log Many | @{allDBs} |
        | Should Contain | ${allDBs} | DBName |
        """
        cur = None
        try:
            allDBs = self._dbconnection.database_names()
            return allDBs
        finally :
            if cur :
                self._dbconnection.end_request() 

    def get_mongodb_collections(self, dbName):
        """
        Returns a list of all of the collections for the database you
        passed in on the connected MongoDB server.

        Usage is:
        | @{allCollections} | Get MongoDB Collections | DBName |
        | Log Many | @{allCollections} |
        | Should Contain | ${allCollections} | CollName |
        """
        cur = None
        try:
            dbName = str(dbName)
            #print "dbName is [ %s ]" % dbName
            #print "dbName is [ %s ]" % type(dbName)
            db = self._dbconnection['%s' % (dbName,)]
            allCollections = db.collection_names()
            return allCollections
        finally :
            if cur :
                self._dbconnection.end_request() 

    def drop_mongodb_database(self, dbDelName):
        """
        Deletes the database passed in from the MongoDB server if it exists.
        If the database does not exist, no errors are thrown.

        Usage is:
        | Drop MongoDB Database | myDB |
        | @{allDBs} | Get MongoDB Collections | myDB |
        | Should Not Contain | ${allDBs} | myDB |
        """
        cur = None
        try:
            dbDelName = str(dbDelName)
            #print "dbDelName is [ %s ]" % dbDelName
            #print "dbDelName is [ %s ]" % type(dbDelName)
            #allResults = self._dbconnection.drop_database('%s' % (dbDelName))
            #return allResults
            self._dbconnection.drop_database('%s' % (dbDelName))
        finally :
            if cur :
                self._dbconnection.end_request() 

    def drop_mongodb_collection(self, dbName, dbCollName):
        """
        Deletes the named collection passed in from the database named.
        If the collection does not exist, no errors are thrown.

        Usage is:
        | Drop MongoDB Collection | myDB | CollectionName |
        | @{allCollections} | Get MongoDB Collections | myDB |
        | Should Not Contain | ${allCollections} | CollectionName |
        """
        cur = None
        try:
            dbName = str(dbName)
            #print "dbName is     [ %s ]" % dbName
            #print "dbName is     [ %s ]" % type(dbName)
            #print "dbCollName is [ %s ]" % dbCollName
            #print "dbCollName is [ %s ]" % type(dbCollName)
            db = self._dbconnection['%s' % (dbName,)]
            db.drop_collection('%s' % (dbCollName))
        finally :
            if cur :
                self._dbconnection.end_request() 

    def validate_mongodb_collection(self, dbName, dbCollName):
        """
        Returns a string of validation info. Raises CollectionInvalid if 
        validation fails.

        Usage is:
        | ${allResults} | Validate MongoDB Collection | DBName | CollectionName |
        | Log | ${allResults} |
        """
        cur = None
        try:
            dbName = str(dbName)
            dbCollName = str(dbCollName)
            #print "dbName is     [ %s ]" % dbName
            #print "dbName is     [ %s ]" % type(dbName)
            #print "dbCollName is [ %s ]" % dbCollName
            #print "dbCollName is [ %s ]" % type(dbCollName)
            db = self._dbconnection['%s' % (dbName,)]
            allResults = db.validate_collection('%s' % dbCollName)
            return allResults
        finally :
            if cur :
                self._dbconnection.end_request() 

    def get_mongodb_collection_count(self, dbName, dbCollName):
        """
        Returns the number records for the collection specified.

        Usage is:
        | ${allResults} | Get MongoDB Collection Count | DBName | CollectionName |
        | Log | ${allResults} |
        """
        cur = None
        try:
            dbName = str(dbName)
            dbCollName = str(dbCollName)
            #print "dbName is     [ %s ]" % dbName
            #print "dbName is     [ %s ]" % type(dbName)
            #print "dbCollName is [ %s ]" % dbCollName
            #print "dbCollName is [ %s ]" % type(dbCollName)
            db = self._dbconnection['%s' % (dbName,)]
            coll = db['%s' % (dbCollName)]
            #print "coll is       [ %s ]" % coll
            count = coll.count()
            return count
        finally :
            if cur :
                self._dbconnection.end_request() 

    def save_mongodb_records(self, dbName, dbCollName, recordJSON):
        """
        If to_save already has an "_id" then an update() (upsert) operation is 
        performed and any existing document with that "_id" is overwritten. 
        Otherwise an insert() operation is performed. In this case if manipulate 
        is True an "_id" will be added to to_save and this method returns the 
        "_id" of the saved document.

        Usage is:
        | ${allResults} | Save MongoDB Records | DBName | CollectionName | JSON |
        | Log | ${allResults} |
        """
        cur = None
        try:
            dbName = str(dbName)
            #print "dbName is             [ %s ]" % dbName
            #print "dbName is             [ %s ]" % type(dbName)
            dbCollName = str(dbCollName)
            #print "dbCollName is         [ %s ]" % dbCollName
            #print "dbCollName is         [ %s ]" % type(dbCollName)
            recordJSON = dict(json.loads(recordJSON))
            #print "recordJSON is         [ %s ]" % recordJSON
            #print "recordJSON is         [ %s ]" % type(recordJSON)
            db = self._dbconnection['%s' % (dbName,)]
            coll = db['%s' % (dbCollName)]
            #print "coll is               [ %s ]" % coll
            #print "type of coll is       [ %s ]" % type(coll)
            allResults = coll.save(recordJSON)
            #print "allResults is         [ %s ]" % allResults
            #print "type of allResults is [ %s ]" % type(allResults)
            return allResults
        finally :
            if cur :
                self._dbconnection.end_request() 

    def retrieve_all_mongodb_records(self, dbName, dbCollName):
        """
        Retrieve ALL of the records in a give MongoDB database collection.

        Usage is:
        | ${allResults} | Retrieve All MongoDB Records | DBName | CollectionName |
        | Log | ${allResults} |
        """
        cur = None
        results = ''
        try:
            dbName = str(dbName)
            dbCollName = str(dbCollName)
            db = self._dbconnection['%s' % (dbName,)]
            coll = db['%s' % (dbCollName)]
            for d in coll.find():
                results = '%s%s' % (results, d.items())
            return results
        finally :
            if cur :
                self._dbconnection.end_request() 

    def retrieve_some_mongodb_records(self, dbName, dbCollName, recordJSON):
        """
        Retrieve some of the records from a given MongoDB database collection
        based on the JSON entered.

        Usage is:
        | ${allResults} | Retrieve Some MongoDB Records | DBName | CollectionName | JSON |
        | Log | ${allResults} |
        """
        cur = None
        results = ''
        try:
            dbName = str(dbName)
            dbCollName = str(dbCollName)
            recordJSON = dict(json.loads(recordJSON))
            #print "dbName is       [ %s ]" % dbName
            #print "dbName is       [ %s ]" % type(dbName)
            #print "dbCollName is   [ %s ]" % dbCollName
            #print "dbCollName is   [ %s ]" % type(dbCollName)
            #print "recordJSON is   [ %s ]" % recordJSON
            #print "recordJSON is   [ %s ]" % type(recordJSON)
            db = self._dbconnection['%s' % (dbName,)]
            coll = db['%s' % (dbCollName)]
            #print "coll is         [ %s ]" % coll
            #print "type of coll is [ %s ]" % type(coll)
            for d in coll.find(recordJSON):
                results = '%s%s' % (results, d.items())
            return results
        finally :
            if cur :
                self._dbconnection.end_request() 

    def remove_mongodb_records(self, dbName, dbCollName, recordJSON):
        """
        Remove some of the records from a given MongoDB database collection
        based on the JSON entered.

        Usage is:
        | ${allResults} | Remove MongoDB Records | DBName | CollectionName | JSON |
        | Log | ${allResults} |
        """
        #  {u'msg': u'Hello 2', u'timestamp': 2, u'_id': ObjectId('4da4a68a52dfbd601b000001')}
        cur = None
        results = ''
        try:
            dbName = str(dbName)
            print "dbName is       [ %s ]" % dbName
            print "dbName is       [ %s ]" % type(dbName)
            dbCollName = str(dbCollName)
            print "dbCollName is   [ %s ]" % dbCollName
            print "dbCollName is   [ %s ]" % type(dbCollName)
            print "recordJSON is   [ %s ]" % recordJSON
            print "recordJSON is   [ %s ]" % type(recordJSON)
            recordJSON = dict(json.loads(recordJSON))
            print "recordJSON is   [ %s ]" % recordJSON
            print "recordJSON is   [ %s ]" % type(recordJSON)
            db = self._dbconnection['%s' % (dbName,)]
            coll = db['%s' % (dbCollName)]
            print "coll is         [ %s ]" % coll
            print "type of coll is [ %s ]" % type(coll)
            allResults = coll.remove(recordJSON)
            return allResults
        finally :
            if cur :
                self._dbconnection.end_request() 

