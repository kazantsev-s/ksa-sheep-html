import sys

import os

INTERP = os.path.expanduser("/var/www/root/data/k62U9r40/bin/python")
if sys.executable != INTERP:
   os.execl(INTERP, INTERP, *sys.argv)

sys.path.append(os.getcwd())

from test import app
