import json
from bson.objectid import ObjectId

class MongoQuery(object):
    """
    Query handles all the querying done by the MongoDB Library. 
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
            print "| @{allDBs} | Get Mongodb Databases |"
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
        db = None
        try:
            dbName = str(dbName)
            db = self._dbconnection['%s' % (dbName,)]
            allCollections = db.collection_names()
            print "| @{allCollections} | Get MongoDB Collections | %s |" % (dbName)
            return allCollections
        finally :
            if db :
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
            print "| Drop MongoDB Database | %s |" % (dbDelName)
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
        db = None
        try:
            dbName = str(dbName)
            db = self._dbconnection['%s' % (dbName,)]
            db.drop_collection('%s' % (dbCollName))
            print "| Drop MongoDB Collection | %s | %s |" % (dbName,dbCollName)
        finally :
            if db :
                self._dbconnection.end_request() 

    def validate_mongodb_collection(self, dbName, dbCollName):
        """
        Returns a string of validation info. Raises CollectionInvalid if 
        validation fails.

        Usage is:
        | ${allResults} | Validate MongoDB Collection | DBName | CollectionName |
        | Log | ${allResults} |
        """
        db = None
        try:
            dbName = str(dbName)
            dbCollName = str(dbCollName)
            db = self._dbconnection['%s' % (dbName,)]
            allResults = db.validate_collection('%s' % dbCollName)
            print "| ${allResults} | Validate MongoDB Collection | %s | %s |" % (dbName,dbCollName)
            return allResults
        finally :
            if db :
                self._dbconnection.end_request() 

    def get_mongodb_collection_count(self, dbName, dbCollName):
        """
        Returns the number records for the collection specified.

        Usage is:
        | ${allResults} | Get MongoDB Collection Count | DBName | CollectionName |
        | Log | ${allResults} |
        """
        db = None
        try:
            dbName = str(dbName)
            dbCollName = str(dbCollName)
            db = self._dbconnection['%s' % (dbName,)]
            coll = db['%s' % (dbCollName)]
            count = coll.count()
            print "| ${allResults} | Get MongoDB Collection Count | %s | %s |" % (dbName,dbCollName)
            return count
        finally :
            if db :
                self._dbconnection.end_request() 

    def save_mongodb_records(self, dbName, dbCollName, recordJSON):
        """
        If to_save already has an "_id" then an update() (upsert) operation is 
        performed and any existing document with that "_id" is overwritten. 
        Otherwise an insert() operation is performed. In this case if manipulate 
        is True an "_id" will be added to to_save and this method returns the 
        "_id" of the saved document.

        | ${allResults} | Save MongoDB Records | DBName | CollectionName | JSON |

        Enter a new record usage is:
        | ${allResults} | Save MongoDB Records | foo | bar | {"timestamp":1, "msg":"Hello 1"} |
        | Log | ${allResults} |

        Update an existing record usage is:
        | ${allResults} | Save MongoDB Records | foo | bar | {"timestamp":1, "msg":"Hello 1"} |
        | Log | ${allResults} |
        """
        db = None
        try:
            dbName = str(dbName)
            dbCollName = str(dbCollName)
            recordJSON = dict(json.loads(recordJSON))
            if recordJSON.has_key('_id'):
                recordJSON['_id']=ObjectId(recordJSON['_id'])
            db = self._dbconnection['%s' % (dbName,)]
            coll = db['%s' % (dbCollName)]
            allResults = coll.save(recordJSON)
            print "| ${allResults} | Save MongoDB Records | %s | %s | %s |" % (dbName,dbCollName,recordJSON)
            return allResults
        finally :
            if db :
                self._dbconnection.end_request() 

    def retrieve_all_mongodb_records(self, dbName, dbCollName, returnDocuments=False):
        """
        Retrieve ALL of the records in a give MongoDB database collection.
        Returned value must be single quoted for comparison, otherwise you will
        get a TypeError error.

        Usage is:
        | ${allResults} | Retrieve All MongoDB Records | DBName | CollectionName |
        | Log | ${allResults} |
        | Should Contain X Times | ${allResults} | '${recordNo1}' | 1 |
        """
        return self._retrieve_mongodb_records(dbName, dbCollName, '{}', returnDocuments)

    def retrieve_some_mongodb_records(self, dbName, dbCollName, recordJSON, returnDocuments=False):
        """
        Retrieve some of the records from a given MongoDB database collection
        based on the JSON entered.
        Returned value must be single quoted for comparison, otherwise you will
        get a TypeError error.

        Usage is:
        | ${allResults} | Retrieve Some MongoDB Records | DBName | CollectionName | JSON |
        | Log | ${allResults} |
        | Should Contain X Times | ${allResults} | '${recordNo1}' | 1 |
        """
        print "| ${allResults} | Retrieve Some MongoDB Records | %s | %s | %s |" % (dbName,dbCollName,recordJSON)
        return self._retrieve_mongodb_records(dbName, dbCollName, recordJSON, returnDocuments)

    def retrieve_mongodb_records_with_desired_fields(self, dbName, dbCollName, recordJSON, fields, return__id=True, returnDocuments=False):
        """
        Retrieves from a document(s) the desired projection. In a sql terms: select a and b from table;
        For more details about querying records from Mongodb and comparison to sql see the
        [http://docs.mongodb.org/manual/reference/sql-comparison|Mongodb]
        documentation.

        In Mongodb terms would correspond: db.collection.find({ }, { fieldA: 1, fieldB: 1 })

        For usage of the dbName, dbCollName and recordJSON arguments, see the keyword
        `Retrieve Some Mongodb Records` documentation.

        fields argument control what field(s) are returned from the document(s),
        it is a comma separated string of fields. It is also possible to return fields
        inside of the array element, by separating field by dot notation. See the
        usage examples for more details how to use fields argument.

        return__id controls is the _id field also returned with the projections.
        Possible values are True and False

        The following usages assume a database name account, collection named users and
        that contain documents of the following prototype:
        {"firstName": "Clark", "lastName": "Kent", "address": {"streetAddress": "21 2nd Street", "city": "Metropolis"}}

        Usage is:
        | ${firstName} | Retrieve MongoDB Records With Desired Fields | account | users | {} | firstName | 0 |
        | ${address} | Retrieve MongoDB Records With Desired Fields | account | users | {} | address | ${false} | # Robot BuiltIn boolean value |
        | ${address_city} | Retrieve MongoDB Records With Desired Fields | account | users | {} | address.city | False |
        | ${address_city_and_streetAddress} | Retrieve MongoDB Records With Desired Fields | account | users | {} | address.city, address.streetAddress | False |
        | ${_id} | Retrieve MongoDB Records With Desired Fields | account | users | {} | firstName | True |
        =>
        | ${firstName} = [(u'firstName', u'Clark')]
        | ${address} = [(u'address', {u'city': u'Metropolis', u'streetAddress': u'21 2nd Street'})]
        | ${address_city} = [(u'address', {u'city': u'Metropolis'})]
        | ${address_city_and_streetAddress} = [(u'address', {u'city': u'Metropolis', u'streetAddress': u'21 2nd Street'})] # Same as retrieving only address
        | ${_id} = [(u'_id', ObjectId('...')), (u'firstName', u'Clark')]

        """
        # Convert return__id to boolean value because Robot Framework returns False/True as Unicode
        try:
            if return__id.isdigit():
                pass
            else:
                return__id = return__id.lower()
                if return__id == 'false':
                    return__id = False
                else:
                    return__id = True
        except AttributeError:
            pass

        # Convert the fields string as a dictionary and handle _id field
        if fields:
            data = {}
            fields = fields.replace(' ', '')
            for item in fields.split(','):
                data[item] = True

            if return__id:
                data['_id'] = True
            elif not return__id:
                data['_id'] = False
            else:
                raise Exception('Not a boolean value for return__id: s%') % (return__id)
        else:
            data = []

        print "| ${allResults} | retreive_mongodb_records_with_desired_fields | %s | %s | %s | %s | %s |" % (dbName, dbCollName, recordJSON, fields, return__id)
        return self._retrieve_mongodb_records(dbName, dbCollName, recordJSON, data, returnDocuments)

    def _retrieve_mongodb_records(self, dbName, dbCollName, recordJSON, fields=[], returnDocuments=False):
        db = None
        try:
            dbName = str(dbName)
            dbCollName = str(dbCollName)
            criteria = dict(json.loads(recordJSON))
            db = self._dbconnection['%s' % (dbName,)]
            coll = db['%s' % (dbCollName)]
            if fields:
                results = coll.find(criteria, fields)
            else:
                results = coll.find(criteria)
            if returnDocuments:
                return list(results)
            else:
                response = ''
                for d in results:
                    response = '%s%s' % (response, d.items())
                return response
        finally :
            if db :
                self._dbconnection.end_request() 

    def remove_mongodb_records(self, dbName, dbCollName, recordJSON):
        """
        Remove some of the records from a given MongoDB database collection
        based on the JSON entered.
        
        The JSON fed in must be double quoted but when doing a comparison, it
        has to be single quoted.  See Usage below
        
        Usage is:
        | ${allResults} | Remove MongoDB Records | ${MDBDB} | ${MDBColl} | {"_id": "4dacab2d52dfbd26f1000000"} |
        | Log | ${allResults} |
        | ${output} | Retrieve All MongoDB Records | ${MDBDB} | ${MDBColl} |
        | Should Not Contain | ${output} | '4dacab2d52dfbd26f1000000' |
        or
        | ${allResults} | Remove MongoDB Records | ${MDBDB} | ${MDBColl} | {"timestamp": {"$lt": 2}} |
        | Log | ${allResults} |
        | ${output} | Retrieve All MongoDB Records | ${MDBDB} | ${MDBColl} |
        | Should Not Contain | ${output} | 'timestamp', 1 |
        """
        db = None
        try:
            dbName = str(dbName)
            dbCollName = str(dbCollName)
            recordJSON = json.loads(recordJSON)
            if recordJSON.has_key('_id'):
                recordJSON['_id']=ObjectId(recordJSON['_id'])
            db = self._dbconnection['%s' % (dbName,)]
            coll = db['%s' % (dbCollName)]
            allResults = coll.remove(recordJSON)
            print "| ${allResults} | Remove MongoDB Records | %s | %s | %s |" % (dbName,dbCollName,recordJSON)
            return allResults
        finally :
            if db :
                self._dbconnection.end_request() 

