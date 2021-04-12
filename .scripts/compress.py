#!/usr/bin/env python3

'''
Read through a directory tree and replace all of the pdf files with compressed versions
Saves a complete backup zip file
Saves a backup of every file that gets compressed, ending in _bak.pdf. These files need to be manually deleted after a check.
'''

import os
import sys
import time
import shutil
import subprocess
#-----------------------------
scriptpath = os.path.dirname(os.path.realpath(__file__))
#-----------------------------
import argparse
parser = argparse.ArgumentParser()
parser.add_argument('-d', '--dir', default='not_specified')
parser.add_argument('-c', '--min_comp_ratio', default=1.2, help="Any compression less than this will be ignored")
parser.add_argument('-b', '--backup_path', default=os.path.expanduser('~/temp'))
args = parser.parse_args()
#-----------------------------
def runcmd(cmd):
	print (cmd)
	subprocess.call(cmd, shell=True)

def replacepdf(thispdf, cr=1.2):
	cfile = os.path.join(os.path.split(thispdf)[0], os.path.split(thispdf)[1].replace(".pdf","_bak.pdf"))
	runcmd('cp "{}" "{}"'.format(thispdf, cfile))
	runcmd('gs -sDEVICE=pdfwrite -dCompatibilityLevel=1.4 -dPDFSETTINGS=/ebook -dNOPAUSE -dQUIET -dBATCH -sOutputFile="{}" "{}"'.format(thispdf, cfile))
	oldsize = os.path.getsize(cfile)
	newsize = os.path.getsize(thispdf)
	print (oldsize, newsize)
	if oldsize < newsize*float(cr) or newsize==0:
		print ("Nothing gained from compression. Leaving alone: {}".format(thispdf))
		runcmd('rm "{}"'.format(thispdf))
		runcmd('mv "{}" "{}"'.format(cfile, thispdf))

#-----------------------------

if not os.path.exists(args.backup_path):
	try:
		os.mkdir(args.backup_path)
	except:
		print ("Exiting. Need working backup_path")
		sys.exit()

dirpath, dirname = os.path.split(args.dir)
backupfile = os.path.join(args.backup_path, "{}_{}.zip".format(dirname,time.strftime("%Y%m%d-%H%M%S")))
runcmd("zip -r {} {}".format(backupfile, args.dir)) # zip recursive, skip hidden files

for root, dirs, files in os.walk(args.dir):
   for name in files:
        if name.endswith(".pdf"):
        	replacepdf(os.path.join(root, name), cr=args.min_comp_ratio)
