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
        
    def disconnect_from_database(self):
        """
        Disconnects from the database.
        
        For example:
        | Disconnect From Database | # disconnects from current connection to the database | 
        """
        #self._dbconnection.close()
        #self._dbconnection.end_request()
        self._dbconnection.disconnect()
        
