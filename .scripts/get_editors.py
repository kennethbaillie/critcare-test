#!/usr/bin/env python3

import os
import re
import datetime
#-----------------------------
import guideline_functions as gl
#-----------------------------
import argparse
parser = argparse.ArgumentParser()
parser.add_argument('-d', '--dir', default='lothiancriticalcare/1a74f8f7b8b7e871b413c4697f68b4401fbacdf0/') # default test dir
parser.add_argument('-v', '--verbose',    action="store_true", default=False,    help='increases verbosity')
args = parser.parse_args()
#-----------------------------
if args.dir == "no_dir_specified":
    print ("no_dir_specified")
    sys.exit()
#-----------------------------
edin = os.path.join(args.dir,"guidelines","offline_EDITORS.txt")
edout = os.path.join(args.dir,"editors.md")
if os.path.exists(edin):
    with open(edin) as f:
        lines=f.readlines()
    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    brackets = re.compile(r"\([^()]*\)$", re.IGNORECASE)
    with open(edout,"w") as o:
        o.write("---\ntitle: Editors\nlayout: page\n---\n\n# Editors\n\n")
        o.write("Last updated {}\n\n".format(now))
        for line in lines:
            o.write("- {}".format(re.sub(brackets, "", line)))

