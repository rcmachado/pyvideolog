import os

from fabric.api import *

def clean():
    current_dir = os.path.dirname(__file__)
    local("find %s -name '*.pyc' -exec rm -f {} \;" % current_dir)
    local("rm -rf %s/build" % current_dir)

def unit(pdb=False):
    pdb_arg = ""
    if pdb:
        pdb_arg = "--pdb"

    clean()
    current_dir = os.path.dirname(__file__)
    command = " ".join(["PYTHONPATH=$PYTHONPATH:%s/videolog" % current_dir,
         "nosetests", pdb_arg, "-s", "--verbose", "--with-coverage",
         "--cover-package=videolog", "tests/unit/*"])
    local(command)
