import os

from fabric.api import *

def unit():
    current_dir = os.path.dirname(__file__)
    command = " ".join(["PYTHONPATH=$PYTHONPATH:%s/videolog" % current_dir,
         "nosetests", "-s", "--verbose", "--with-coverage",
         "--cover-package=videolog", "tests/unit/*"])
    local(command)
