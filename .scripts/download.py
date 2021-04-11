#!/usr/bin/env python3

import os
import sys
import json
import shutil
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
    print (folder_url)
    print (html)
    line = [l for l in html.split("\n") if "prefetch-shared_link_folder_entries-ShmodelFolderEntriesPrefetch-1" in l][0]
    json_data = line.split("responseReceived(")[1].replace(")});", "").replace('\\', '"').replace('""', '"')[1:-1]
    data = json.loads(json_data)
    return [link["url"] for link in data["shared_link_infos"]]

def download_files_from_dir(dir_name, folder_url):
    urls = get_document_urls_from_url(folder_url)
    for url in urls:
        base_url = url.split('?')[0]
        filename = urllib.parse.unquote(base_url).split('/')[-1]
        destinationfile = os.path.join(dir_name, filename)
        if not os.path.exists(dir_name):
            os.makedirs(dir_name, exist_ok=True)
        if "." in filename:
            file_url = base_url + '?dl=1'
            print("Downloading file:", file_url)
            r = requests.get(file_url)
            with open(destinationfile, 'wb') as f:
                f.write(r.content)
        else:
            # then this is a directory. Download the whole shebang
            destinationdir = os.path.join(dir_name, filename)
            print ("Downloading subdirectory:", filename)
            download_files_from_dir(destinationdir, url)

if os.path.exists(args.destinationdir):
    shutil.rmtree(args.destinationdir)
download_files_from_dir(args.destinationdir, args.sourcedir)







