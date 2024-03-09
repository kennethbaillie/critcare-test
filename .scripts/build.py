#!/usr/bin/env python3

import os
import sys
import subprocess
import oyaml as yaml
#-----------------------------
import argparse
parser = argparse.ArgumentParser()
parser.add_argument('-f', '--force_errors',    action="store_true", default=False,    help='carries on if errors happen')
parser.add_argument('-o', '--override_changes', default=False, action="store_true")
parser.add_argument('-v', '--verbose', default=False, action="store_true")
parser.add_argument('-r', '--getreviewdates', default=False, action="store_true")
args = parser.parse_args()
#-----------------------------
path_to_top_level = "../"
sourcefile = "_data/guidelinesets.yml"
scriptpath = os.path.dirname(os.path.realpath(__file__))
#-----------------------------
class cd:
    def __init__(self, newPath):
        self.newPath = os.path.expanduser(newPath)
    def __enter__(self):
        self.savedPath = os.getcwd()
        os.chdir(self.newPath)
    def __exit__(self, etype, value, traceback):
        os.chdir(self.savedPath)

def run_command(command, force=False):
    print (command)
    try:
        subprocess.run(command, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error occurred: {e}")
        if force:
            pass    
        else:
            print ("Stopping due to error")
            sys.exit()

def run_build(directory, secret, cloudlink):
    secretdir = directory + "/" + secret
    publicdir = directory + "/public"
    oc = ""
    verbose = ""
    if args.verbose:
        verbose = "-v"
    if args.override_changes:
        oc = "-o"
    run_command(f"python3 .scripts/make_robots.py {verbose}")
    run_command(f"python3 .scripts/download.py -s '{cloudlink}' -d '{secretdir}/' {verbose}", force=args.force_errors)
    run_command(f"python3 .scripts/makelist.py -e -d '{secretdir}/' {oc} {verbose}", force=args.force_errors)
    run_command(f"python3 .scripts/get_duplicates.py -d '{secretdir}/' {oc} {verbose}", force=args.force_errors)
    run_command(f"python3 .scripts/get_editors.py -d '{secretdir}/' {verbose}", force=args.force_errors)
    if args.getreviewdates:
        run_command(f"python3 .scripts/get_review_dates.py -d '{secretdir}/' {oc} {verbose}", force=args.force_errors)
    run_command(f"git add -v {secretdir}/*", force=args.force_errors)
    run_command(f"git add -v {publicdir}/*", force=True)
#-----------------------------

run_command(f"git config --local user.email 'action@github.com'", force=args.force_errors)
run_command(f"git config --local user.name 'GitHub Action'", force=args.force_errors)
with cd(os.path.join(scriptpath, path_to_top_level)):
    with open(sourcefile) as f:
        text = f.read()
    yml = yaml.load(text, Loader=yaml.Loader)
    for guidelineset in yml:
        run_build(
            guidelineset["directory"],
            guidelineset["secret"],
            guidelineset["cloudlink"],
            )






