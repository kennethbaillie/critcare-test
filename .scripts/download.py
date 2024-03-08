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
from msal import ConfidentialClientApplication
#-----------------------------
import guideline_functions as gl
#-----------------------------
import argparse
parser = argparse.ArgumentParser()
parser.add_argument('-s', '--sourcedir', default='https://www.dropbox.com/sh/w9jw30h9bj5cbh2/AACEcqEc-_9Sl6J6g0pveapba?dl=0') # default test dir
parser.add_argument('-d', '--destinationdir', default='lothiancriticalcare/1a74f8f7b8b7e871b413c4697f68b4401fbacdf0/guidelines/', help="relative path from top level directory of jekyll site")
parser.add_argument('-w', '--webstem', default='https://critcare.net/')
parser.add_argument('-c', '--cloud', default='dropbox')
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
changelog = os.path.abspath(os.path.join(args.destinationdir,"../",".changes.json")) # same as makelist.py
#-----------------------------

# UNTESTED CODE FOR ONE DRIVE 

def get_access_token(client_id, client_secret, tenant_id):
    authority = f"https://login.microsoftonline.com/{tenant_id}"
    app = ConfidentialClientApplication(client_id, client_secret=client_secret, authority=authority)
    scopes = ["https://graph.microsoft.com/.default"]
    result = app.acquire_token_for_client(scopes)
    if "access_token" in result:
        return result["access_token"]
    else:
        raise ValueError("Error obtaining access token: ", result.get("error_description"))

def download_file(url, local_path):
    response = requests.get(url, stream=True)
    response.raise_for_status()
    with open(local_path, "wb") as local_file:
        for chunk in response.iter_content(chunk_size=8192):
            local_file.write(chunk)

def download_onedrive_contents(shared_link, local_folder, client_id, client_secret, tenant_id):
    access_token = get_access_token(client_id, client_secret, tenant_id)
    headers = {"Authorization": f"Bearer {access_token}"}
    # Resolve shared link and get driveId and itemId
    shared_link_info = requests.get(f"https://graph.microsoft.com/v1.0/shares/{shared_link}/driveItem", headers=headers).json()
    drive_id = shared_link_info["parentReference"]["driveId"]
    item_id = shared_link_info["id"]
    # Get the directory contents
    directory_contents = requests.get(f"https://graph.microsoft.com/v1.0/drives/{drive_id}/items/{item_id}/children", headers=headers).json()
    # Download the files
    for item in directory_contents["value"]:
        if item["file"]:
            download_url = item["@microsoft.graph.downloadUrl"]
            local_path = os.path.join(local_folder, item["name"])
            print(f"Downloading {item['name']} to {local_path}")
            download_file(download_url, local_path)

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
            if args.verbose:
                print (target)
                print (p)
            try:
                out = '{}: [Link]({}{}{})'.format(
                                    p.relative_to(pathlib.PurePosixPath(args.destinationdir)), 
                                    args.webstem,
                                    args.destinationdir,
                                    gl.fix_filename(p.relative_to(pathlib.PurePosixPath(args.destinationdir))),
                                    )
            except:
                out = '{}'.format(p.relative_to(pathlib.PurePosixPath(args.destinationdir)))
                print ("Error: unable to get printable path for {}. Continuing.".format(target))
    else:
        out = '{}'.format(p.relative_to(pathlib.PurePosixPath(args.destinationdir)))
    return out

def try_remove(thistarget):
    if args.verbose: print ("==> Trying to remove:", thistarget)
    if os.path.isdir(thistarget):
        try:
            shutil.rmtree(thistarget)
            if args.verbose: print ("==> successfully removed (shutil):", thistarget)
        except:
            print ("Unable to remove this directory ({}): {}".format(sys.exc_info()[0],thistarget))
    else:
        try:
            os.remove(thistarget)
            if args.verbose: print ("==> successfully removed (os):", thistarget)
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
def download_files_from_dir(folder_url, dir_name, temp, cloud=args.cloud):
    if cloud == "dropbox":
        download_dropbox_folder(folder_url, temp)
    elif cloud == "onedrive":
        client_id = os.environ["ONEDRIVE_CLIENT_ID"] # register these with github 
        client_secret = os.environ["ONEDRIVE_CLIENT_SECRET"]
        tenant_id = os.environ["ONEDRIVE_TENANT_ID"]
        download_onedrive_contents(folder_url, temp, client_id, client_secret, tenant_id)
    comparison = filecmp.dircmp(dir_name, temp, ignore=gl.ignorelist+gl.exclude_from_reports, hide=gl.ignorelist+gl.exclude_from_reports)
    target = os.path.basename(os.path.normpath(dir_name))
    record_diffs(comparison)
    action_diffs(comparison)

#-----------------------------
# create temp dir, download all to it, parse and then remove
tempdir = os.path.join(args.destinationdir, ".temp")
if not os.path.exists(tempdir):
    os.makedirs(tempdir, exist_ok=True)
    if args.verbose:
        print ("cloud data downloaded to {}".format(tempdir))
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
            outputc[category][targetfile.replace("/.temp/","/")] = printablepath(changes[category][targetfile], link=True) # switch new/changed filepaths to online directory
        elif category == "renamed":
            outputc[category][targetfile.replace("/.temp/","/")] = "{} ==> {}".format(
                                                                        printablepath(targetfile),
                                                                        printablepath(changes[category][targetfile], link=True)
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
        print(outputc)
        print("successfully written to {}".format(changelog))











