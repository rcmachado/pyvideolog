import os

from fabric.api import *

def clean():
    current_dir = os.path.dirname(__file__)
    local("find %s -name '*.pyc' -exec rm -f {} \;" % current_dir)
    local("rm -rf %s/build" % current_dir)

def unit():
    clean()
    current_dir = os.path.dirname(__file__)
    command = " ".join(["PYTHONPATH=$PYTHONPATH:%s/videolog" % current_dir,
         "nosetests", "-s", "--verbose", "--with-coverage",
         "--cover-package=videolog", "tests/unit/*"])
    local(command)
