import os
import sys
import json
from datetime import datetime
#-----------------------------
import argparse
parser = argparse.ArgumentParser()
parser.add_argument('-d', '--destinationdir', default='no_dir_specified')
args = parser.parse_args()
#-----------------------------
if args.destinationdir == "no_dir_specified":
    print ("no_dir_specified")
    sys.exit()
#-----------------------------
changelog = os.path.join(args.destinationdir,".changes.json")
outputfile = os.path.join(args.destinationdir,"../changes.html")

if not os.path.exists(changelog):
    print ("no changelog file found at: {}".format(changelog))
    sys.exit()
print (outputfile)

with open(changelog) as f:
    changes = json.load(f)

now = datetime.now() 
newtext = "\n<hr><h3>{}</h3><br>\n".format(now.strftime("%d/%m/%Y %H:%M:%S"))
for thistype in changes:
    if len(changes[thistype]) > 0:
        newtext += "<h4>{}</h4>\n".format(thistype)
        for file in changes[thistype]:
            newtext += "<p>{}: <a href='{}'>link</a></p>\n".format(file, changes[thistype][file])

oldtext = ""
if os.path.exists(outputfile):
    with open(outputfile) as f:
        oldtext = f.read()

with open(outputfile,"w") as o:
    o.write(newtext + oldtext)

os.remove(changelog)
