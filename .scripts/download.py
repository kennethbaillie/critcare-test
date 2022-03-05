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
parser.add_argument('-s', '--sourcedir', default='https://www.dropbox.com/sh/otczbgim2zkeub8/AACru2-Xv6w2qFAwsz6fSi0Ja?dl=0') # default edu folder only
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

def action_diffs(dcmp, targetdirname):
    global changes
    targetdirname = targetdirname.replace("/","")
    for name in dcmp.left_only:
        target = os.path.join(dcmp.left, name)
        print("deleted file {}".format(target))
        try_remove(target)
        changes["deleted"][target.split("/{}/".format(targetdirname))[1]] = makelink(target)
    for name in dcmp.right_only:
        target = os.path.join(dcmp.left, name)
        print("new file {}".format(target))
        if os.path.isdir(os.path.join(dcmp.right, name)):
            shutil.copytree(os.path.join(dcmp.right, name), target)
        else:
            shutil.copy2(os.path.join(dcmp.right, name), target)
        changes["new"][target.split("/{}/".format(targetdirname))[1]] = makelink(target)
    for name in dcmp.diff_files:
        target = os.path.join(dcmp.left, name)
        print("changed file {}".format(target))
        shutil.copy2(os.path.join(dcmp.right, name), target)
        changes["modified"][target.split("/{}/".format(targetdirname))[1]] = makelink(target)
    # search for renamed files, which will appear to be both deleted and new
    print ("Renamed search underway now")
    for dfile in changes["deleted"]:
        print (dfile)
        for nfile in changes["new"]:
            print (dfile, nfile, filecmp.cmp(dfile, nfile))


    for sub_dcmp in dcmp.subdirs.values():
        action_diffs(sub_dcmp, targetdirname)

filecmp.dircmp
def download_files_from_dir(folder_url, dir_name, td):
    download_dropbox_folder(folder_url, td)
    comparison = filecmp.dircmp(dir_name, td, ignore=ignorelist, hide=ignorelist)
    td = os.path.basename(os.path.normpath(dir_name))
    print ("td", td)
    action_diffs(comparison, td)

#-----------------------------

# create temp dir, download all to it, parse and then remove
tempdir = os.path.join(args.destinationdir, ".temp")
if not os.path.exists(tempdir):
    os.makedirs(tempdir, exist_ok=True)
changes = {"deleted":{},"modified":{},"new":{}}
download_files_from_dir(args.sourcedir, args.destinationdir, tempdir)
##### commented out 
#try_remove(tempdir)

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










