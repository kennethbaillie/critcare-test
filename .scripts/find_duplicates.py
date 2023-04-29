#!/usr/bin/env python3

import os
import datetime
import os
import hashlib
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
        if name in gl.ignorelist+gl.exclude_from_comparisons:
            return False
    return True

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
                if pdf_text:
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

with gl.cd(args.sourcedir):
    dups = find_duplicate_pdfs("./")
    print ("Unfiltered duplicates:")
    printdups(dups)
    dups = [x for x in dups if reportable_duplicate(x[0]) and reportable_duplicate(x[1])]
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
        o.write("\n".join(["{} == {}".format(x[0],x[1]) for x in dups]))














