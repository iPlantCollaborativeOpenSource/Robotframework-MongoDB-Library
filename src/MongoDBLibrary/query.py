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
        """
        cur = None
        try:
            dbName = str(dbName)
            print "dbName is [%s]" % dbName
            print "dbName is [%s]" % type(dbName)
            db = self._dbconnection['%s' % (dbName,)]
            allCollections = db.collection_names()
            return allCollections
        finally :
            if cur :
                self._dbconnection.end_request() 
