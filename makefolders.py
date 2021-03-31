import re
import os
import sys
import subprocess

scriptpath = os.path.dirname(os.path.realpath(__file__))
#-----------------------------
import argparse
parser = argparse.ArgumentParser()
parser.add_argument('-d', '--dir', default=os.path.join(scriptpath,'docs/criticalcare/'))
parser.add_argument('-o', '--outputfile', default=os.path.join(scriptpath,'docs/list.html'))
parser.add_argument('-i', '--indexfile', default=os.path.join(scriptpath,'docs/index.json'))
parser.add_argument('-b', '--basedir', default=os.path.join(scriptpath,'docs'))
parser.add_argument('-f', '--fast', default=False, action="store_true")
args = parser.parse_args()
#-----------------------------
excluded = ['Icon']
def accept(file_or_dir_name):
    if file_or_dir_name.startswith('.'):
        return False
    if file_or_dir_name.strip() in excluded:
        return False
    return True
#-----------------------------
topdirlist = [x for x in sorted(os.listdir(args.dir)) if accept(x)]

print (topdirlist)

for tld in topdirlist:
	cmd = "mkdir {}/offline_DRAFTS".format(os.path.join(scriptpath,'docs/criticalcare/',tld))
	print (cmd)
	subprocess.call(cmd, shell=True)