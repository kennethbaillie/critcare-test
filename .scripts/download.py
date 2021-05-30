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

def download_files_from_dir(folder_url, dir_name, td):
    urls = get_document_urls_from_url(folder_url)
    if not os.path.exists(dir_name):
        os.makedirs(dir_name, exist_ok=True)
    deleted_files = [x for x in os.listdir(dir_name) if x not in [getfilenamefromdropbox(y) for y in urls] and not x.startswith(".")]
    for d in deleted_files:
        try:
            os.remove(os.path.join(dir_name, d))
        except:
            print ("Unable to remove this file ({}): {}".format(sys.exc_info()[0],os.path.join(dir_name, d)))
        changes["deleted"][d] = 1
    for url in urls:
        filename = getfilenamefromdropbox(url)
        print ("filename: ", filename)
        destinationfile = os.path.join(dir_name, filename)
        if "." in filename:
            tempfile = os.path.join(td, filename)
            print("Downloading file:{}\nto location:{}".format(url, tempfile))
            r = requests.get(url)
            with open(tempfile, 'wb') as f:
                f.write(r.content)
            if os.path.exists(destinationfile):
                print (filecmp.cmp(tempfile, destinationfile))
                if filecmp.cmp(tempfile, destinationfile):
                    print ("files identical")
                else:
                    print ("files not identical")
                    shutil.copy2(tempfile, destinationfile)
                    changes["changed"][destinationfile] = 1
            else:
                print ("new file")
                shutil.copy2(tempfile, destinationfile)
                changes["new"][destinationfile] = 1
            os.remove(tempfile)
        else:
            # then this is a directory. Download the whole shebang
            destinationdir = os.path.join(dir_name, filename)
            print("Downloading subdirectory:{}\nto location:{}".format(filename, destinationdir))
            download_files_from_dir(url, destinationdir, td)
#-----------------------------

tempdir = os.path.join(args.destinationdir, "temp")
if not os.path.exists(tempdir):
    os.makedirs(tempdir, exist_ok=True)

changelog = os.path.join(args.destinationdir,".changes.json")
if os.path.exists(changelog):
    with open(changelog) as f:
        changes = json.load(f)
else:
    changes = {
        "deleted":{},
        "changed":{},
        "new":{},
    }

download_files_from_dir(args.sourcedir, args.destinationdir, tempdir)

with open(changelog,"w") as o:
    changes = json.dump(o, indent=4)















