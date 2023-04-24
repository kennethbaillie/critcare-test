#!/usr/bin/env python3

import os
import sys
import json
import copy
import shutil
import pathlib
import filecmp
import requests
import urllib.parse
from zipfile import ZipFile
#-----------------------------
import guideline_functions as gl
#-----------------------------
import argparse
parser = argparse.ArgumentParser()
parser.add_argument('-s', '--sourcedir', default='https://www.dropbox.com/sh/3jornh1s315cxzj/AAC_2OF49UbxYMo-gEHN0liWa?dl=0') # default test dir
parser.add_argument('-d', '--destinationdir', default='../docs/test_secret/criticalcare/')
parser.add_argument('-w', '--webstem', default='https://critcare.net/')
parser.add_argument('-v', '--verbose',    action="store_true", default=False,    help='increases verbosity')
args = parser.parse_args()
#-----------------------------
if args.sourcedir == "no_dir_specified":
    print ("no_dir_specified")
    sys.exit()
#-----------------------------
changestoignore = [
        "editors.md",
    ]
#-----------------------------
changelog = os.path.join(args.destinationdir,".changes.json")
#-----------------------------
def download_dropbox_folder(folder_url, dest):
    # download whole dropbox folder as zip file
    zf = os.path.join(dest,"temp.zip")
    folder_url = folder_url.replace("?dl=0","?dl=1")
    r = requests.get(folder_url, stream=True)
    with open(zf, 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024): 
            if chunk:
                f.write(chunk)
    with ZipFile(zf, 'r') as zipObj:
        zipObj.extractall(dest)

def printablepath(target, link=False):
    target = target.replace("/.temp/","/")
    p = pathlib.PurePosixPath(target)
    if link:
        if os.path.isdir(p):
            out = '{}: [folder]'.format(p.relative_to(pathlib.PurePosixPath(args.destinationdir)))
        else:
            out = '{}: <a href="{}{}">Link</a>'.format(
                                    p.relative_to(pathlib.PurePosixPath(args.destinationdir)), 
                                    args.webstem,
                                    p.relative_to(pathlib.PurePosixPath('docs')),
                                    )
    else:
        out = '{}'.format(p.relative_to(pathlib.PurePosixPath(args.destinationdir)))
    return out

def try_remove(thistarget):
    if args.verbose: print ("==> Trying to remove:", thistarget)
    if os.path.isdir(thistarget):
        try:
            shutil.rmtree(thistarget)
        except:
            print ("Unable to remove this directory ({}): {}".format(sys.exc_info()[0],thistarget))
    else:
        try:
            os.remove(thistarget)
        except:
            print ("Unable to remove this file ({}): {}".format(sys.exc_info()[0],thistarget))

def record_diffs(dcmp):
    global changes
    # RECORD changes
    for name in dcmp.left_only:
        if name not in changestoignore:
            dfile = os.path.join(dcmp.left, name)
            if args.verbose: print ("==> deleted file {}".format(dfile))
            changes["deleted"][dfile]=dfile
    for name in dcmp.right_only:
        if name not in changestoignore:
            nfile = os.path.join(dcmp.right, name)
            if args.verbose: print ("==> new file {}".format(nfile))
            changes["new"][nfile]=nfile
    for name in dcmp.diff_files:
        if name not in changestoignore:
            cfile = os.path.join(dcmp.right, name)
            if args.verbose: print ("==> changed file {}".format(cfile))
            changes["modified"][cfile]=cfile
    if args.verbose: print ("==> Renamed search underway now", dcmp.left_only, dcmp.right_only)
    for dfile in copy.copy(list(changes["deleted"].keys())):
        for nfile in copy.copy(list(changes["new"].keys())):
            if args.verbose: print ("==> ", dfile, nfile, filecmp.cmp(dfile, nfile))
            if filecmp.cmp(dfile, nfile):
                changes["renamed"][dfile] = nfile
                if dfile in changes["deleted"].keys():
                    del changes["deleted"][dfile]
                if nfile in changes["new"].keys():
                    del changes["new"][nfile]
    for i, sub_dcmp in enumerate(dcmp.subdirs.values()):
        if args.verbose: print ("==> Iterating over subdirectory: ", list(dcmp.subdirs.keys())[i])
        record_diffs(sub_dcmp)

def action_diffs(dcmp):
    # ENACT changes
    for name in dcmp.left_only: # remove deleted files from online (left) folder
        try_remove(os.path.join(dcmp.left, name))
    for name in dcmp.right_only:# add new directories or files from right to online (left) folder
        if os.path.isdir(os.path.join(dcmp.right, name)):
            shutil.copytree(os.path.join(dcmp.right, name), os.path.join(dcmp.left, name))
        else:
            shutil.copy2(os.path.join(dcmp.right, name), os.path.join(dcmp.left, name))
    for name in dcmp.diff_files: # copy changed files from right to left folder
        shutil.copy2(os.path.join(dcmp.right, name), os.path.join(dcmp.left, name))
    # look in subdirectories
    for i, sub_dcmp in enumerate(dcmp.subdirs.values()):
        if args.verbose: print ("==> Iterating over subdirectory: ", list(dcmp.subdirs.keys())[i])
        action_diffs(sub_dcmp)

#filecmp.dircmp
def download_files_from_dir(folder_url, dir_name, temp):
    download_dropbox_folder(folder_url, temp)
    comparison = filecmp.dircmp(dir_name, temp, ignore=gl.ignorelist+gl.exclude_from_comparisons, hide=gl.ignorelist+gl.exclude_from_comparisons)
    target = os.path.basename(os.path.normpath(dir_name))
    record_diffs(comparison)
    action_diffs(comparison)

#-----------------------------
# create temp dir, download all to it, parse and then remove
tempdir = os.path.join(args.destinationdir, ".temp")
if not os.path.exists(tempdir):
    os.makedirs(tempdir, exist_ok=True)
changes = {"deleted":{},"modified":{},"new":{},"renamed":{}}
outputc = {"deleted":{},"modified":{},"new":{},"renamed":{}}
download_files_from_dir(args.sourcedir, args.destinationdir, tempdir)
try_remove(tempdir)

outputc = {}
for category in changes:
    outputc[category]={}
    if args.verbose: print("\n==> Changes:", category)
    for targetfile in changes[category]:
        if args.verbose: print("\t- (category) ", targetfile)
        if category =="deleted":
            outputc[category][targetfile.replace("/.temp/","/")] = printablepath(changes[category][targetfile]) 
        elif category == "new" or category == "modified":
            outputc[category][targetfile.replace("/.temp/","/")] = printablepath(changes[category][targetfile],link=True) # switch new/changed filepaths to online directory
        elif category == "renamed":
            outputc[category][targetfile.replace("/.temp/","/")] = "{} ==> {}".format(
                                                                        printablepath(targetfile),
                                                                        printablepath(changes[category][targetfile])
                                                                    )
# record changes by adding them to existing json file
try:   
    with open(changelog) as f:
        stored_changes = json.load(f)
except:
    stored_changes = {}
for category in outputc:
    try:
        outputc[category] = outputc[category] | stored_changes[category]
    except:
        pass
with open(changelog,"w") as o:
    json.dump(outputc, o, indent=4)
    if args.verbose: 
        print("The following changelog:")
        print(changelog)
        print("successfully written to {outputc}")











