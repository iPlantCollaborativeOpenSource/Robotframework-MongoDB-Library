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

