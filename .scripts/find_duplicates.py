#!/usr/bin/env python3

import os
import datetime
import find_duplicate_files
#-----------------------------
import guidelines as gl
#-----------------------------
import argparse
parser = argparse.ArgumentParser()
parser.add_argument('-s', '--sourcedir', default='docs/test_secret') # default test dir
parser.add_argument('-v', '--verbose',    action="store_true", default=False,    help='increases verbosity')
args = parser.parse_args()
#-----------------------------
if args.sourcedir == "no_dir_specified":
    print ("no_dir_specified")
    sys.exit()

dupout = os.path.join(args.sourcedir,"duplicates.md")

with gl.cd(args.sourcedir):
    dups = find_duplicate_files.find_duplicate_files("./")
    for ignorefile in gl.ignorelist:
        dups = [x for x in dups if ignorefile not in [os.path.split(y)[1] for y in x]]

with open(dupout,"w") as o:
    o.write("---\ntitle:Duplicates\n---\n\n# Duplicates\n\n")
    if len(dups)==0:
        o.write("No duplicate files found on {}".format(datetime.today().strftime('%Y-%m-%d %H:%M:%S')))
    else:
        o.write("\n".join(["{} : {}".format(x[0],x[1]) for x in dups]))














