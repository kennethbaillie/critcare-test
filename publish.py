import os
import sys
import platform
import subprocess

#-----------------------------
sourcedir = os.path.expanduser("~/Dropbox/6_websites/rie_app/site/")
extradir = os.path.expanduser("~/Dropbox/6_websites/rie_app/extradir/")
secure_source = os.path.expanduser("~/Dropbox/6_websites/rie_app/secure/")
#-----------------------------
destination1 = "sidies:/home/borismit/public_html/rie.app/"
secure_destination1 = os.path.expanduser("sidies:/home/borismit/.htpasswds/public_html/rie.app/")
#-----------------------------
destination2 = "sidies:/home/borismit/public_html/critcare.net/"
secure_destination2 = os.path.expanduser("sidies:/home/borismit/.htpasswds/public_html/critcare.net/")
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
	cmd = "{} build".format(mkdocs)
	subprocess.call(cmd, shell=True)

	if len(extradir) > 1:
		cmd = "rsync --update -avzp {} {}".format(extradir, sourcedir)
		subprocess.call(cmd, shell=True)

	#-----------------------------
	cmd = "rsync -avzp {} -e ssh {} --rsync-path /home/borismit/rsync/rsync-3.1.2/rsync".format(sourcedir, destination1)
	subprocess.call(cmd, shell=True)

	if len(secure_source) > 1:
		cmd = "rsync -avzp {} -e ssh {}  --rsync-path /home/borismit/rsync/rsync-3.1.2/rsync ".format(secure_source, secure_destination1)
		subprocess.call(cmd, shell=True)
	#-----------------------------

	cmd = "rsync -avzp {} -e ssh {} --rsync-path /home/borismit/rsync/rsync-3.1.2/rsync".format(sourcedir, destination2)
	subprocess.call(cmd, shell=True)

	if len(secure_source) > 1:
		cmd = "rsync -avzp {} -e ssh {}  --rsync-path /home/borismit/rsync/rsync-3.1.2/rsync ".format(secure_source, secure_destination2)
		subprocess.call(cmd, shell=True)
	#-----------------------------










