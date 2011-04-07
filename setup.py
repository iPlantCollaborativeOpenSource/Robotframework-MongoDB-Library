#!/usr/bin/env python

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


"""Setup script for Robot's MongoDBLibrary distributions"""

from distutils.core import setup

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from MongoDBLibrary import __version__

def main():
    setup(name         = 'robotframework-mongodblibrary',
          version      = __version__,
          description  = 'MongoDB Database library for Robot Framework',
          author       = 'Jerry Schneider',
          author_email = 'jerry57@gmail.com',
          url          = 'https://github.com/jerry57/Robotframework-MongoDB-Library',
          package_dir  = { '' : 'src'},
          packages     = ['MongoDBLibrary']
          )
        

if __name__ == "__main__":
    main()
