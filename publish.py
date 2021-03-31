import os
import sys
import platform
import subprocess

#-----------------------------
maindir = os.path.expanduser("~/Dropbox/6_websites/critcare.net/")
extradir = ""
secure_source = os.path.expanduser("~/Dropbox/6_websites/critcare.net/secure/")
#-----------------------------
destination = "sidies:/home/borismit/public_html/critcare.net/"
secure_destination = os.path.expanduser("sidies:/home/borismit/.htpasswds/public_html/critcare.net/")
#-----------------------------
scriptpath = os.path.dirname(os.path.realpath(__file__))
#-----------------------------
mkdocs = "mkdocs"
if platform.system() == "Linux":
	mkdocs = "/home/kbaillie/anaconda3/envs/jkb37/bin/mkdocs"
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
def getyaml(name, filepath):
	with open(filepath) as f:
		for x in f.readlines():
			line = x.split(':')
			if line[0].strip() == name and len(x)>1:
				return line[1].strip()
#-----------------------------

sourcedir = getyaml('site_dir', os.path.join(maindir, 'mkdocs.yml'))
if not sourcedir:
	print ("error! site dir not identified in:", os.path.join(maindir, 'mkdocs.yml'))
	print ("bailing out")
	sys.exit()
if not sourcedir.endswith('/'):
	sourcedir += "/" # necessary for rsync to work properly

with cd(scriptpath):
	cmd = "{} build".format(mkdocs)
	subprocess.call(cmd, shell=True)

	if len(extradir) > 1:
		cmd = "rsync --update -avzp {} {}".format(extradir, sourcedir)
		subprocess.call(cmd, shell=True)

	#-----------------------------

	cmd = "rsync -avzp {} -e ssh {} --rsync-path /home/borismit/rsync/rsync-3.1.2/rsync".format(sourcedir, destination)
	subprocess.call(cmd, shell=True)

	if len(secure_source) > 1:
		cmd = "rsync -avzp {} -e ssh {}  --rsync-path /home/borismit/rsync/rsync-3.1.2/rsync ".format(secure_source, secure_destination)
		subprocess.call(cmd, shell=True)
	#-----------------------------










