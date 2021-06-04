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
parser.add_argument('-s', '--sourcedir', default='no_dir_specified')
parser.add_argument('-d', '--destinationdir', default='no_dir_specified')
args = parser.parse_args()
#-----------------------------
if args.sourcedir == "no_dir_specified":
    print ("no_dir_specified")
    sys.exit()
#-----------------------------
changelog = os.path.join(args.destinationdir,".changes.json")
#-----------------------------
ignorelist = [
        "temp.zip",
        "offline_DRAFTS",
        ".DS_Store",
        ".temp",
        "temp",
        ".changes.json",
        "changes.html",
        "__MACOSX",
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

def try_remove(thisfile):
    try:
        os.remove(thisfile)
    except:
        print ("Unable to remove this file ({}): {}".format(sys.exc_info()[0],thisfile))

def action_diffs(dcmp):
    global changes
    for name in dcmp.left_only:
        target = os.path.join(dcmp.left, name)
        print("deleted file {}".format(target))
        try_remove(target)
        changes["deleted"][target.split("/criticalcare/")[1]] = makelink(target)
    for name in dcmp.right_only:
        target = os.path.join(dcmp.left, name)
        print("new file {}".format(target))
        shutil.copy2(os.path.join(dcmp.right, name), target)
        changes["new"][target.split("/criticalcare/")[1]] = makelink(target)
    for name in dcmp.diff_files:
        target = os.path.join(dcmp.left, name)
        print("changed file {}".format(target))
        shutil.copy2(os.path.join(dcmp.right, name), target)
        changes["modified"][target.split("/criticalcare/")[1]] = makelink(target)
    for sub_dcmp in dcmp.subdirs.values():
        action_diffs(sub_dcmp)

def download_files_from_dir(folder_url, dir_name, td):
    download_dropbox_folder(folder_url, td)
    comparison = filecmp.dircmp(dir_name, td, ignore=ignorelist)
    action_diffs(comparison)

#-----------------------------

tempdir = os.path.join(args.destinationdir, ".temp")
if not os.path.exists(tempdir):
    os.makedirs(tempdir, exist_ok=True)

changes = {
    "deleted":{},
    "modified":{},
    "new":{},
}

if os.path.exists(changelog):
    try:   
        with open(changelog) as f:
            changes = json.load(f)
    except:
        pass

download_files_from_dir(args.sourcedir, args.destinationdir, tempdir)

with open(changelog,"w") as o:
    json.dump(changes, o, indent=4)















