#!/usr/bin/env python3

import os
import sys
import json
import shutil
import filecmp
import pathlib
import requests
import urllib.parse
from zipfile import ZipFile

#-----------------------------
import argparse
parser = argparse.ArgumentParser()
parser.add_argument('-s', '--sourcedir', default='https://www.dropbox.com/sh/7m3txr3zwy2nrf7/AADmjUlNgm78GD60FMT9PNNQa?dl=0') # default test dir
parser.add_argument('-d', '--destinationdir', default='docs/test_secret/criticalcare/')
args = parser.parse_args()
#-----------------------------
if args.sourcedir == "no_dir_specified":
    print ("no_dir_specified")
    sys.exit()
#-----------------------------
changelog = os.path.join(args.destinationdir,".changes.json")
#-----------------------------
# files to ignore in comparison
ignorelist = [
        "temp.zip",
        ".DS_Store",
        ".temp",
        "temp",
        ".changes.json",
        "changes.html",
        "__MACOSX",
        "offline_DRAFTS",
        "Emergencies",
    ]

def makelink(target):
    p = pathlib.PurePosixPath(target)
    link = "https://critcare.net/{}".format(p.relative_to('docs'))
    return link

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

def try_remove(thistarget):
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

def action_diffs(dcmp):
    global changes
    for name in dcmp.left_only:
        dfile = os.path.join(dcmp.left, name)
        print("deleted file {}".format(dfile))
        changes["deleted"][dfile] = makelink(dfile)
    for name in dcmp.right_only:
        nfile = os.path.join(dcmp.left, name)
        print("new file {}".format(name))
        if os.path.isdir(os.path.join(dcmp.right, name)):
            shutil.copytree(os.path.join(dcmp.right, name), nfile)
        else:
            shutil.copy2(os.path.join(dcmp.right, nfile), nfile)
        changes["new"][target.split("/{}/".forma))[1]] = makelink(target)
    for name in dcmp.diff_files:
        target = os.path.join(dcmp.left, name)
        print("changed file {}".format(target))
        shutil.copy2(os.path.join(dcmp.right, name), target)
        changes["modified"][target.split("/{}/".forma))[1]] = makelink(target)
    # search for renamed files, which will appear to be both deleted and new
    print ("Renamed search underway now", dcmp.left_only, dcmp.right_only)
    for dfile in changes["deleted"]:
        for nfile in changes["new"]:
            print (dfile, nfile, filecmp.cmp(dfile, nfile))
        try_remove(dfile)


    for i, sub_dcmp in enumerate(dcmp.subdirs.values()):
        print ("iterating over subdirectory: ", list(dcmp.subdirs.keys())[i])
        action_diffs(sub_dcmp)

#filecmp.dircmp
def download_files_from_dir(folder_url, dir_name, temp):
    download_dropbox_folder(folder_url, temp)
    comparison = filecmp.dircmp(dir_name, temp, ignore=ignorelist, hide=ignorelist)
    target = os.path.basename(os.path.normpath(dir_name))
    print ("temp", temp)
    print ("target", target)
    action_diffs(comparison, target)

#-----------------------------

# create temp dir, download all to it, parse and then remove
tempdir = os.path.join(args.destinationdir, ".temp")
if not os.path.exists(tempdir):
    os.makedirs(tempdir, exist_ok=True)
changes = {"deleted":{},"modified":{},"new":{}}
download_files_from_dir(args.sourcedir, args.destinationdir, tempdir)
#try_remove(tempdir)


changes["deleted"][target.split("/{}/".format(targetdirname))[1]] = makelink(target)

# record changes by adding them to existing json file
try:   
    with open(changelog) as f:
        stored_changes = json.load(f)
except:
    stored_changes = {}
c={}
for d in changes:
    if d in stored_changes:
        c[d] = changes[d] | stored_changes[d] #Python 3.9 merging dictionaries
    else:
        c[d] = changes[d]
with open(changelog,"w") as o:
    json.dump(c, o, indent=4)










