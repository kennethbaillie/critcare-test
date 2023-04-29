#!/usr/bin/env python3

import os
import sys
import time
import datetime
import hashlib
#-----------------------------
import guideline_functions as gl
#-----------------------------
import argparse
parser = argparse.ArgumentParser()
parser.add_argument('-s', '--sourcedir', default='docs/test_secret') # default test dir
parser.add_argument('-v', '--verbose',    action="store_true", default=False,    help='increases verbosity')
parser.add_argument('-o', '--override_changes', default=False, action="store_true")
args = parser.parse_args()
#-----------------------------
if args.sourcedir == "no_dir_specified":
    print ("no_dir_specified")
    sys.exit()
#-----------------------------

def get_file_hash(text):
    return hashlib.md5(text.encode('utf-8')).hexdigest()

def find_duplicate_pdfs(root_dir):
    file_hashes = {}
    duplicates = []
    for dirpath, _, filenames in os.walk(root_dir):
        for filename in filenames:
            if filename.lower().endswith('.pdf'):
                file_path = os.path.join(dirpath, filename)
                pdf_text = gl.get_pdf_text(file_path)
                print (filename)
                if pdf_text:
                    print ("text acquired")
                    file_hash = get_file_hash(pdf_text)
                    if file_hash in file_hashes:
                        duplicates.append([file_path, file_hashes[file_hash]])
                    else:
                        file_hashes[file_hash] = file_path
    return duplicates

def printdups(dups):
    for dup in dups:
        print (dup)

dupout = os.path.join(args.sourcedir,"../duplicates.md")
changes_record_file = os.path.join(args.sourcedir,"../changes.html")

if not (gl.newchanges(changes_record_file) or args.override_changes):
    print ("Stopping because {} hasn't changed.".format(os.path.abspath(changes_record_file)))
    sys.exit()

with gl.cd(args.sourcedir):
    dups = find_duplicate_pdfs("./")
    print ("Unfiltered duplicates:")
    printdups(dups)
    dups = [x for x in dups if gl.is_reportable(x[0]) and gl.is_reportable(x[1])]
    for dirnamestartstring in ["Emergencies", ".", ".temp"]:
        filtered_duplicates = [(path1, path2) for path1, path2 in dups if not any(dir_name.startswith(dirnamestartstring) for dir_name in path1.split(os.path.sep) + path2.split(os.path.sep))]
    print ("\nFinal duplicates:")
    printdups(dups)

now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
with open(dupout,"w") as o:
    o.write("---\ntitle: Duplicates\n---\n\n# Duplicates\n\n")
    if len(dups)==0:
        o.write("No duplicate files found on {}".format(now))
    else:
        o.write("Duplicates found ({}):\n\n".format(now))
        o.write("\n".join(["- {} == {}".format(x[0],x[1]) for x in dups]))














