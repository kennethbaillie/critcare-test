#!/usr/bin/env python3

import os
import sys
import json
import shutil
import filecmp
import requests
import urllib.parse

#-----------------------------
import argparse
parser = argparse.ArgumentParser()
parser.add_argument('-s', '--sourcedir', default='no_dir_specified')
parser.add_argument('-d', '--destinationdir', default='no_dir_specified')
args = parser.parse_args()
#-----------------------------

def get_document_urls_from_url(folder_url):
    r = requests.get(folder_url)
    html = r.content.decode('utf8')
    line = [l for l in html.split("\n") if "prefetch-shared_link_folder_entries-ShmodelFolderEntriesPrefetch-1" in l][0]
    json_data = line.split("responseReceived(")[1].replace(")});", "").replace('\\', '"').replace('""', '"')[1:-1]
    data = json.loads(json_data)
    filelist = [link["url"] for link in data["shared_link_infos"]]
    return filelist

def getfilenamefromdropbox(url):
    url = url.split('?')[0]
    return urllib.parse.unquote(url).split('/')[-1]

def try_remove(thisfile):
    try:
        os.remove(thisfile)
    except:
        print ("Unable to remove this file ({}): {}".format(sys.exc_info()[0],thisfile))

def download_files_from_dir(folder_url, dir_name, td):
    urls = get_document_urls_from_url(folder_url)
    if not os.path.exists(dir_name):
        os.makedirs(dir_name, exist_ok=True)
    deleted_files = [x for x in os.listdir(dir_name) if x not in [getfilenamefromdropbox(y) for y in urls] and not x.startswith(".")]
    for d in deleted_files:
        dpath = os.path.join(dir_name, d)
        try_remove(dpath)
        changes["deleted"][dpath] = 1
    for url in urls:
        filename = getfilenamefromdropbox(url)
        tempfile = os.path.join(td, filename)
        destinationfile = os.path.join(dir_name, filename)
        if "." in filename:
            dl_url = url.split('?')[0] + '?dl=1' # changes dl=0 to dl=1 so that dropbox allows download
            print("Downloading file:{}\nto location:{}".format(dl_url, tempfile))
            r = requests.get(dl_url)
            with open(tempfile, 'wb') as f:
                f.write(r.content)
            # now check if the file exists or has changed
            if os.path.exists(destinationfile):
                print (filecmp.cmp(tempfile, destinationfile))
                if filecmp.cmp(tempfile, destinationfile):
                    print ("files identical")
                else:
                    print ("files modified")
                    shutil.copy2(tempfile, destinationfile)
                    changes["modified"][destinationfile] = 1
            else:
                print ("new file")
                shutil.copy2(tempfile, destinationfile)
                changes["new"][destinationfile] = 1
            try_remove(tempfile)
        else:
            # then this is a directory. Download the whole shebang
            destinationdir = os.path.join(dir_name, filename)
            print("Downloading subdirectory:{}\nto location:{}".format(filename, destinationdir))
            download_files_from_dir(url, destinationdir, td)
#-----------------------------

tempdir = os.path.join(args.destinationdir, ".temp")
if not os.path.exists(tempdir):
    os.makedirs(tempdir, exist_ok=True)

changes = {
    "deleted":{},
    "modified":{},
    "new":{},
}
changelog = os.path.join(args.destinationdir,".changes.json")
if os.path.exists(changelog):
    try:   
        with open(changelog) as f:
            changes = json.load(f)
    except:
        pass

download_files_from_dir(args.sourcedir, args.destinationdir, tempdir)

with open(changelog,"w") as o:
    json.dump(changes, o, indent=4)















