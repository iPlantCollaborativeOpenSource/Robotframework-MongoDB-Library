#!/usr/bin/env python

"""Setup script for Robot's MongoDB Library distributions"""

from distutils.core import setup

import sys, os
sys.path.insert(0, os.path.join('src','MongoDBLibrary'))

from version import VERSION

def main():
    setup(name         = 'robotframework-mongodblibrary',
          version      = VERSION,
          description  = 'Mongo Database utility library for Robot Framework',
          author       = 'Jerry Schneider',
          author_email = 'jerry@iplantcollaborative.org',
          url          = 'https://github.com/',
          package_dir  = { '' : 'src'},
          packages     = ['MongoDBLibrary']
          )
        

if __name__ == "__main__":
    main()
