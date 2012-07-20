#  Copyright (c) 2012 Jerry Schneider
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

from mongo_connection_manager import MongoConnectionManager
from mongoquery import MongoQuery
from version import VERSION

#__version__ = '0.1'

class MongoDBLibrary(MongoConnectionManager, MongoQuery):
    """
    MongoDB Library contains utilities meant for Robot Framework's usage.
    
    This can allow you to query your Mongo database after an action has been made to verify the results.
    
    
    
    References:
    
     + PyMongo 2.2 Documentation - http://api.mongodb.org/python/2.2/
     
    Notes:
    
    
    
    Example Usage:
    | # Setup |
    | Connect to Database |
    | # Guard assertion (verify that test started in expected state). |
    | Check if not exists in database | select id from person where first_name = 'Franz Allan' and last_name = 'See' |
    | # Drive UI to do some action | 
    | Go To | http://localhost/person/form.html | | # From selenium library |
    | Input Text |  name=first_name | Franz Allan | # From selenium library |
    | Input Text |  name=last_name | See | # From selenium library |
    | Click Button | Save | | # From selenium library |
    | # Log results | 
    | @{queryResults} | Query | select * from person |
    | Log Many | @{queryResults} |
    | # Verify if persisted in the database |
    | Check if exists in database | select id from person where first_name = 'Franz Allan' and last_name = 'See' |
    | # Teardown |
    | Disconnect from Database | 
    """
    
    ROBOT_LIBRARY_SCOPE = 'GLOBAL'
    ROBOT_LIBRARY_VERSION = VERSION

