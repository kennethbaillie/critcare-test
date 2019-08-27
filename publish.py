#!/opt/local/bin/python
# -*- coding: UTF-8 -*-
#version 2

import os
import platform
import subprocess
#-----------------------------
sourcedir = os.path.expanduser("~/Dropbox/6_websites/rie_app/site/")
extradir = os.path.expanduser("~/Dropbox/6_websites/rie_app/extradir/")
destination = "sidies:/home/borismit/public_html/rie.app/"
#-----------------------------
scriptpath = os.path.dirname(os.path.realpath(__file__))
#-----------------------------
mkdocs = "mkdocs"
if platform.system() == "Linux":
	mkdocs = '/home/kbaillie/anaconda3/bin/mkdocs'
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
with cd(scriptpath):
	cmd = "python {}".format(os.path.join(scriptpath, 'makelist.py'))
	subprocess.call(cmd, shell=True)

	cmd = "{} build".format(mkdocs)
	subprocess.call(cmd, shell=True)

	if len(extradir) > 1:
		cmd = "rsync --update -avzp {} {}".format(extradir, sourcedir)
		subprocess.call(cmd, shell=True)

	cmd = "rsync -avzp {} -e ssh {} --rsync-path /home/borismit/rsync/rsync-3.1.2/rsync".format(sourcedir, destination)
	subprocess.call(cmd, shell=True)
	#-----------------------------


