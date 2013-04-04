
- Unit test are defined in the src/unit/test_*.py files
- Currently each test suite spans a subprocess of the mongo db in the setUp
- It is assumed that each unit test will do independently:
    * Set up all required database(s), collections and documents in collection 
    * Clean all that is done is test setup
    * There are mongo_* functions for these purposes

- Unit test are run from src/unit folder by executing command:  python -m unittest discover
- For more details hot to run different unit test (suites), see python unit test documentation [1]. 


TODO: 
Unit test setUp good benefit some refactoring:
1) All of the def mongo_* functions could be placed in some other file, when this one unit test file is divided
2) Also starting up the mongo database could be a separate class all together 
3) Also some cored could take a look and see if unit test written by tester make any sense at all.
4) Currently running unit test requires python 2.7 or in older version unittest2 [2] is required. Some automatic detection would be nice

[1] http://docs.python.org/2/library/unittest.html#command-line-interface
[2] https://pypi.python.org/pypi/unittest2