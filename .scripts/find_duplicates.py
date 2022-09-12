#!/usr/bin/env python3

import os
import datetime
import find_duplicate_files
#-----------------------------
import guideline_functions as gl
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
#-----------------------------

def recursive_split(s):
    stem, name = list(os.path.split(s))
    if stem in ['', os.path.sep]:
        return [name]
    return recursive_split(stem) + [name]

def reportable_duplicate(thispath, verbose=True):
    dir_and_file_names = recursive_split(thispath)
    if "." in dir_and_file_names:
        dir_and_file_names.remove('.')
    for name in dir_and_file_names:
        if not gl.accept("", name):
            return False
    return True

dupout = os.path.join(args.sourcedir,"../duplicates.md")

with gl.cd(args.sourcedir):
    dups = find_duplicate_files.find_duplicate_files("./")
    dups = [x for x in dups if reportable_duplicate(x[0]) and reportable_duplicate(x[1])]
    print (dups)

now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
with open(dupout,"w") as o:
    o.write("---\ntitle: Duplicates\n---\n\n# Duplicates\n\n")
    if len(dups)==0:
        o.write("No duplicate files found on {}".format(now))
    else:
        o.write("Duplicates found ({}):\n\n".format(now))
        o.write("\n".join(["{} == {}".format(x[0],x[1]) for x in dups]))














