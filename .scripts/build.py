#!/usr/bin/env python3

import os
import sys
import subprocess
import oyaml as yaml
#-----------------------------
import argparse
parser = argparse.ArgumentParser()
parser.add_argument('-f', '--force_errors',    action="store_true", default=False,    help='carries on if errors happen')
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

def run_build(directory, cloudlink):
    run_command(f"python .scripts/download.py -v -s '{cloudlink}' -d '{directory}/guidelines/'", force=args.force_errors)
    run_command(f"python .scripts/makelist.py -d '{directory}/' -e", force=args.force_errors)
    run_command(f"python .scripts/get_duplicates.py -d '{directory}/'", force=args.force_errors)
    run_command(f"python .scripts/get_review_dates.py -d '{directory}/'", force=args.force_errors)
    run_command(f"python .scripts/get_editors.py -d '{directory}/'", force=args.force_errors)
    run_command(f"git add -v {directory}/*", force=args.force_errors)
    run_command(f"git add -v public/*", force=True)
#-----------------------------

run_command(f"git config --local user.email 'action@github.com'", force=args.force_errors)
run_command(f"git config --local user.name 'GitHub Action'", force=args.force_errors)
with cd(os.path.join(scriptpath, path_to_top_level)):
    with open(sourcefile) as f:
        text = f.read()
    yml = yaml.load(text, Loader=yaml.Loader)
    for guidelineset in yml:
        run_build(
            guidelineset["directory"] + "/" + guidelineset["secret"],
            guidelineset["cloudlink"],
            )






