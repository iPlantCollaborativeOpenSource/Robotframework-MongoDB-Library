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

#import ConfigParser
#import pymongo

class ConnectionManager(object):
    """
    Connection Manager handles the connection & disconnection to the database.
    """

    def __init__(self):
        """
        Initializes _dbconnection to None.
        """
        self._dbconnection = None
        
    def connect_to_mongodb(self, dbHost='localhost', dbPort=27017, dbPoolSize=None, dbAutoStart=None, dbTimeout=None, dbSlaveOkay=False, dbNetworkTimeout=None, dbDocClass=dict, dbTZAware=False):
        #class pymongo.connection.Connection([host='localhost'[, port=27017[, pool_size=None[, auto_start_request=None[, timeout=None[, slave_okay=False[, network_timeout=None[, document_class=dict[, tz_aware=False]]]]]]]]])
        """
        Loads pymongo and connects to the MongoDB host using parameters submitted.
        
        Example usage:
        | # To connect to foo.bar.org's MongoDB service on port 27017 |
        | Connect To MongoDB | foo.bar.org | ${27017} |
        
        """
        dbapiModuleName = 'pymongo'
        db_api_2 = __import__(dbapiModuleName);
        
        dbPort = int(dbPort)
        print "host is               [%s]" % dbHost
        print "port is               [%s]" % dbPort
        print "pool_size is          [%s]" % dbPoolSize
        print "auto_start_request is [%s]" % dbAutoStart
        print "timeout is            [%s]" % dbTimeout
        print "slave_okay is         [%s]" % dbSlaveOkay
        print "document_class is     [%s]" % dbDocClass
        print "tz_aware is           [%s]" % dbTZAware
        
        self._dbconnection = db_api_2.connection.Connection (host=dbHost, port=dbPort, pool_size=dbPoolSize, auto_start_request=dbAutoStart, timeout=dbTimeout, slave_okay=dbSlaveOkay, network_timeout=dbNetworkTimeout, document_class=dbDocClass, tz_aware=dbTZAware);
        
    def disconnect_from_mongodb(self):
        """
        Disconnects from the MongoDB server.
        
        For example:
        | Disconnect From MongoDB | # disconnects from current connection to the MongoDB server | 
        """
        self._dbconnection.disconnect()
        
