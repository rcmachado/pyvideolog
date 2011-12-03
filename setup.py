# -*- coding: utf-8 -*-
import os
from setuptools import setup, find_packages

from videolog import __version__

# Utility function to read the README file.  
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = 'videolog',
    version = __version__,
    description = "Python module to access Videolog's API",
    long_description = read('README.md'),
    keywords = ['videolog'],
    author = 'Rodrigo Machado',
    author_email = 'rcmachado@gmail.com',
    url = 'http://github.com/rcmachado/pyvideolog',
    license = 'MIT',
    classifiers = ['Development Status :: 4 - Beta',
                   'Intended Audience :: Developers',
                   'License :: OSI Approved :: MIT License',
                   'Natural Language :: English',
                   'Natural Language :: Portuguese (Brazilian)',
                   'Operating System :: POSIX :: Linux',
                   'Programming Language :: Python :: 2.5',
                   'Programming Language :: Python :: 2.6',
                   'Topic :: Software Development :: Libraries :: Application Frameworks',
                   ],
    packages = find_packages(),
    package_dir = {"videolog": "videolog"},
    requires=['simplexml (>=0.1.4)'],
    include_package_data = True,
    test_suite="nose.collector",
)
