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
import pymongo

class ConnectionManager(object):
    """
    Connection Manager handles the connection & disconnection to the database.
    """

    def __init__(self):
        """
        Initializes _dbconnection to None.
        """
        self._dbconnection = None
        
    def connect_to_dbapi2(self, dbapiModuleName, *args):
    #class pymongo.connection.Connection([host='localhost'[, port=27017[, pool_size=None[, auto_start_request=None[, timeout=None[, slave_okay=False[, network_timeout=None[, document_class=dict[, tz_aware=False]]]]]]]]])
        """
        Loads the DB API 2.0 module with the given `dbapiModuleName`, then uses
        it to connect to the database using `args`. The arguments depend on the
        dbapiModule which is used for the connection.
        Example usage:
        | # Using psycopg2, specify postgres database name, user and password |
        | Connect To Dbapi2 | psycopg2 | my_db | user | s3cr3t |
        | # Using pymysql, specify mysql database host, user, password, db and port |
        | Connect To Dbapi2 | pymysql | localhost | user | s3cr3t | my_db | 3306 |

        | # Using jaydebeapi, set classpath, connect via jdbc driver in Python or Jython |
        | Set Environment Variable | CLASSPATH | ${CURDIR}/../libraries/ojdbc14-10.2.0.3.0.jar |
        | Connect To Dbapi2 | jaydebeapi | oracle.jdbc.driver.OracleDriver | jdbc:oracle:thin:@host:port | user | s3cr3t |

        """
        db_api_2 = __import__(dbapiModuleName);
        # TODO: pass configfile as second arg dbConfigFile="./resources/db.cfg"?
        # maybe use ConfigParser.SafeConfigParser({'bar': 'Life', 'baz': 'hard'})
        # seems to be recommended by Python reference
        # don't know how to handle config.items so that it can be passed as args
        self._dbconnection = db_api_2.connection.Connection (*args);
        
    def connect_to_mongodb(self, dbHost='localhost', dbPort=27017, dbPoolSize=None, dbAutoStart=None, dbTimeout=None, dbSlaveOkay=False, dbNetworkTimeout=None, dbDocClass=dict, dbTZAware=False):
    #class pymongo.connection.Connection([host='localhost'[, port=27017[, pool_size=None[, auto_start_request=None[, timeout=None[, slave_okay=False[, network_timeout=None[, document_class=dict[, tz_aware=False]]]]]]]]])
        """
        Loads the DB API 2.0 module with the given `dbapiModuleName`, then uses
        it to connect to the database using `args`. The arguments depend on the
        dbapiModule which is used for the connection.
        Example usage:
        | # Using psycopg2, specify postgres database name, user and password |
        | Connect To Dbapi2 | psycopg2 | my_db | user | s3cr3t |
        | # Using pymysql, specify mysql database host, user, password, db and port |
        | Connect To Dbapi2 | pymysql | localhost | user | s3cr3t | my_db | 3306 |

        | # Using jaydebeapi, set classpath, connect via jdbc driver in Python or Jython |
        | Set Environment Variable | CLASSPATH | ${CURDIR}/../libraries/ojdbc14-10.2.0.3.0.jar |
        | Connect To Dbapi2 | jaydebeapi | oracle.jdbc.driver.OracleDriver | jdbc:oracle:thin:@host:port | user | s3cr3t |

        """
        dbapiModuleName = 'pymongo'
        db_api_2 = __import__(dbapiModuleName);
        # TODO: pass configfile as second arg dbConfigFile="./resources/db.cfg"?
        # maybe use ConfigParser.SafeConfigParser({'bar': 'Life', 'baz': 'hard'})
        # seems to be recommended by Python reference
        # don't know how to handle config.items so that it can be passed as args
        dbPort = int(dbPort)
        #print "dbapiModuleName is    [%s]" % dbapiModuleName
        #print "dbHost is             [%s]" % dbHost
        #print "dbPort is             [%s]" % dbPort
        #print "dbPoolSize is         [%s]" % dbPoolSize
        #print "dbAutoStart is        [%s]" % dbAutoStart
        #print "dbTimeout is          [%s]" % dbTimeout
        #print "dbSlaveOkay is        [%s]" % dbSlaveOkay
        #print "dbDocClass is         [%s]" % dbDocClass
        #print "dbTZAware is          [%s]" % dbTZAware
        print "host is               [%s]" % dbHost
        print "port is               [%s]" % dbPort
        print "pool_size is          [%s]" % dbPoolSize
        print "auto_start_request is [%s]" % dbAutoStart
        print "timeout is            [%s]" % dbTimeout
        print "slave_okay is         [%s]" % dbSlaveOkay
        print "document_class is     [%s]" % dbDocClass
        print "tz_aware is           [%s]" % dbTZAware

        #self._dbconnection = db_api_2.connection.Connection ([host=dbHost[, port=dbPort[, pool_size=dbPoolSize[, auto_start_request=dbAutoStart[, timeout=dbTimeout[, slave_okay=dbSlaveOkay[, network_timeout=dbNetworkTimeout[, document_class=dbDocClass[, tz_aware=dbTZAware]]]]]]]]]);
        self._dbconnection = db_api_2.connection.Connection (host=dbHost, port=dbPort, pool_size=dbPoolSize, auto_start_request=dbAutoStart, timeout=dbTimeout, slave_okay=dbSlaveOkay, network_timeout=dbNetworkTimeout, document_class=dbDocClass, tz_aware=dbTZAware);
        
    def disconnect_from_mongodb(self):
        """
        Disconnects from the database.
        
        For example:
        | Disconnect From Database | # disconnects from current connection to the database | 
        """
        #self._dbconnection.close()
        #self._dbconnection.end_request()
        self._dbconnection.disconnect()
        
