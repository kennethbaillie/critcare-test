#!/usr/bin/env python3

import os
import subprocess
import oyaml as yaml
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

def run_command(command):
    print (command)
    subprocess.run(command, shell=True, check=True)

def run_build(directory, cloudlink):
    run_command(f"python .scripts/download.py -v -s '{cloudlink}' -d '{directory}/guidelines/'")
    run_command(f"python .scripts/makelist.py -d '{directory}/' -e")
    run_command(f"python .scripts/get_duplicates.py -d '{directory}/'")
    run_command(f"python .scripts/get_review_dates.py -d '{directory}/'")
    run_command(f"python .scripts/get_editors.py -d '{directory}/'")
    run_command(f"git add -v {directory}/*")
    run_command(f"git add -v public/*")
#-----------------------------

run_command(f"git config --local user.email 'action@github.com'")
run_command(f"git config --local user.name 'GitHub Action'")
with cd(os.path.join(scriptpath, path_to_top_level)):
    with open(sourcefile) as f:
        text = f.read()
    yml = yaml.load(text, Loader=yaml.Loader)
    for guidelineset in yml:
        run_build(
            guidelineset["directory"] + "/" + guidelineset["secret"],
            guidelineset["cloudlink"],
            )






