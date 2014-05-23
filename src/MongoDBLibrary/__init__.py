from mongo_connection_manager import MongoConnectionManager
from mongoquery import MongoQuery
from version import VERSION

class MongoDBLibrary(MongoConnectionManager, MongoQuery):
    """
    MongoDB Library contains utilities meant for Robot Framework's usage.
    
    This can allow you to query your Mongo database after an action has been made to verify the results.
    
    
    
    References:
    
     + PyMongo 2.2 Documentation - http://api.mongodb.org/python/2.2/
     
    Notes:
    
    
    
    Example Usage:
    | # ToDo |
    """
    
    ROBOT_LIBRARY_SCOPE = 'GLOBAL'
    ROBOT_LIBRARY_VERSION = VERSION

