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
args = parser.parse_args()
#-----------------------------
path_to_top_level = "../"
robotfile = "robots.txt"
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
#-----------------------------

disallowed = []
with cd(os.path.join(scriptpath, path_to_top_level)):
    with open(sourcefile) as f:
        text = f.read()
    yml = yaml.load(text, Loader=yaml.Loader)
    for guidelineset in yml:
        disallowed.append("*/"+guidelineset["secret"]+"/*")

with cd(os.path.join(scriptpath, path_to_top_level)):
    with open(robotfile) as f:
        lines = [line.strip() for line in f.readlines()]
    outlines = []
    dl = "Disallow:"
    for line in lines:
        if line.startswith(dl):
            disallowed.append(line.replace(dl,"").strip())
        else:
            outlines.append(line)
    disallowed = list(set(disallowed))
    outlines += ["{} {}".format(dl,x) for x in disallowed]
    with open(robotfile, "w") as o:
        o.write("\n".join(outlines))






