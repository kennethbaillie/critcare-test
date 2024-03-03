﻿#!/usr/bin/env python3

'''
Makes an html list of pdf files in a directory
Also makes a lunr search index


TODO: make the formatting of search links use the same function as the formatting of list links so that e.g. videos work
'''
import re
import os
import sys
import json
import shutil
import subprocess
from datetime import datetime
#-----------------------------
import guideline_functions as gl
#-----------------------------
scriptpath = os.path.dirname(os.path.realpath(__file__))
#-----------------------------
import argparse
parser = argparse.ArgumentParser()
parser.add_argument('-d', '--dir', default=os.path.join(scriptpath,'../lothiancriticalcare/1a74f8f7b8b7e871b413c4697f68b4401fbacdf0/'))
parser.add_argument('-f', '--fast', default=False, action="store_true")
parser.add_argument('-o', '--override_changes', default=False, action="store_true")
parser.add_argument('-b', '--backgroundcolor', default="#f5f5f5") #bdfcec
parser.add_argument('-e', '--do_emergency', default=False, action="store_true")
parser.add_argument('-p', '--pin_to_top',    action='append', default=[], help='use this to append as many values as you want')
parser.add_argument('-lf', '--listfilename', default='list.html')
parser.add_argument('-if', '--indexfilename', default='index.json')
parser.add_argument('-ed', '--emergencydirname', default='Emergencies')
parser.add_argument('-gd', '--guidelinesdirname', default='guidelines')
parser.add_argument('-pd', '--publicdirname', default='public')
args = parser.parse_args()
#-----------------------------
guidelinesdir = os.path.join(args.dir, args.guidelinesdirname)
publicdir = os.path.join(args.dir, "..", args.publicdirname)
#-----------------------------
changelog = os.path.join(args.dir,".changes.json")
changes_record_file = os.path.join(args.dir,"changes.html")
dupout = os.path.join(args.dir,"duplicate_titles.md")
globalsynonymsfile = os.path.join(args.dir,"synonyms.json") # ovararching synonyms file. May also create individual ones for each folder in future.
#-----------------------------

def get_unique_words(bigstring):
    global gsyn
    deletelist = [
        '\ufb01',
        '\u00e2',
        '\u2021',
        '\u2013',
        '\ufb02',
        '\ufb02',
        '\ufb00',
        '\u201c',
        '\u201d',
        '\u2018',
        '\u2019',
        '\u2265',
        '\u2191',
        '\u2022',
        '\u00a3',
        '\u00fc',
        '\u00a0',
        '\u00e1',
        '\uf0a3',
        '\u00f8',
        '\u2026',
        '\ufffd',
        '\u00ef',
        ]
    for char in deletelist:
        bigstring = bigstring.replace(char,'')
    for char in ['\t','.','[',']','(',')','{','}','"',"'","/","\\",'-',':','!','_']:
        bigstring = bigstring.replace(char,' ')
    bs = [x.strip() for x in re.split(';| |,|\n|\r',bigstring)]
    bs = list(set([x.lower() for x in bs if len(x)>1]))
    for synonymlist in gsyn:
        bs = [" ".join(synonymlist) if x in synonymlist else x for x in bs]
    return ' '.join(bs)

def make_search_entry(thisfile, thisbasedir, indexfilename=args.indexfilename):
    if args.fast:
        return
    thistitle = fixname(os.path.split(thisfile)[1])
    linktarget = thisfile
    if thisfile.endswith(".md"):
        linktarget = thisfile[:-3]
    new_entry = {
        'href': os.path.relpath(linktarget, thisbasedir),
        'title': thistitle,
        'content': get_unique_words(gl.readfilecontents(thisfile)), # this is the slow bit
        }
    jsonpath = os.path.join(thisbasedir, indexfilename)
    with open(jsonpath) as f:
        sl = json.load(f)
    sl.append(new_entry)
    with open(jsonpath,"w") as o:
        json.dump(sl, o, indent=4)

def eclass(filename):
    if filename.strip().lower() == args.emergencydirname.strip().lower():
        return "emergency"
    emlabels = ["_em.", "_em_"]
    for x in emlabels:
        if x in filename:
            return "emergency"
    return ""

def is_public(filepath):
    thispath, filename = os.path.split(filepath)
    if not(gl.accept(thispath, filename)):
        return False
    if os.path.isdir(filepath):
        return True
    emlabels = ["_pub.", "_pub_"]
    for x in emlabels:
        if x in filename:
            return True
    return False

def ignore_files(folder, files):
    ''' for shutils copytree '''
    return [f for f in files if not is_public(os.path.join(folder, f))]

def fixname(thisname):
    labels = ["_em","_pub"]
    for x in labels:
        thisname = thisname.replace(x+".", ".")
        thisname = thisname.replace(x+"_", "_")
    thisname = thisname.replace("_"," ").split('.')[0]
    return thisname

def makeid(thisname):
    return ''.join(thisname.split())
def formatfilelink(thisdir, entry, basedir, depth=0):
    linktext = ""
    if gl.accept(thisdir, entry):
        if entry.endswith('.md'):
            linktarget = entry.replace(".md","") # md files automatically converted by mkdocs
            print ("md", thisdir, entry, linktarget)
            linktext += ('''
                <a class='{}' href='{}'>
                    <li class='list-group-item' style='margin-left:{}em;'>{}</li>
                </a>
                '''.format(
                    eclass(entry),
                    os.path.relpath(os.path.join(thisdir, linktarget), basedir),
                    depth,
                    fixname(entry))
                    )
        else:
            linktext += ('''
                <a class='{}' href='{}'>
                    <li class='list-group-item' style='margin-left:{}em;'>{}</li>
                </a>
                '''.format(
                    eclass(entry),
                    os.path.relpath(os.path.join(thisdir, entry), basedir),
                    depth,
                    fixname(entry))
                    )
        make_search_entry(os.path.join(thisdir, entry), basedir)
        return linktext

def formatdir(thisdir, basedir, depth=0):
    text = ''
    for entry in sorted(os.listdir(thisdir)):
        if not gl.accept(thisdir, entry):
            continue
        if os.path.isdir(os.path.join(thisdir, entry)):
            text += ('''
                <div class="accordion-item">
                    <h2 class="accordion-header" id="heading{}">
                        <button class="accordion-button {}" type="button" data-bs-toggle="collapse" data-bs-target="#collapse{}" aria-expanded="true" aria-controls="collapse{}" style='margin-left:{}em;'>
                            {}
                        </button>
                    </h2>
                    <div id="collapse{}" class="accordion-collapse collapse" aria-labelledby="heading{}" data-bs-parent="#accordion">
                        <div class="accordion-body">
                            <ul class='list-group'>{}</ul>
                        </div>
                    </div>
                </div>
                '''.format(
                    makeid(entry),
                    eclass(entry),
                    makeid(entry),
                    makeid(entry),
                    depth,
                    fixname(entry),
                    makeid(entry),
                    makeid(entry),
                    formatdir(os.path.join(thisdir, entry), basedir, depth+1)
                    )
                )
        else:
            text += formatfilelink(thisdir, entry, basedir, depth)
    return text

def makelist(fromdir=guidelinesdir, listfile=args.listfilename, indexfile=args.indexfilename):
    i = 0
    basedir = os.path.abspath(os.path.join(fromdir, ".."))
    searchindexfile = os.path.join(basedir, indexfile)
    if not args.fast:
        with open(searchindexfile, "w") as o:
            json.dump([], o, indent=4)
    uncategorised = []
    listfiletext = '<div class="accordion" id="accordion">\n'
    topdirlist = [x for x in sorted(os.listdir(fromdir)) if x not in args.pin_to_top]
    topdirlist = args.pin_to_top + topdirlist
    for d in topdirlist:
        if not(gl.accept(fromdir, d)):
            continue
        if os.path.isdir(os.path.join(fromdir, d)):
            listfiletext += ('''
                <div class="accordion-item">
                    <h2 class="accordion-header" id="heading{}">
                        <button class="accordion-button {}" type="button" data-bs-toggle="collapse" data-bs-target="#collapse{}" aria-expanded="true" aria-controls="collapse{}">
                            <div class="accordion-body" style="background: {};">
                                {}
                            </div>
                        </button>
                    </h2>
                    <div id="collapse{}" class="accordion-collapse collapse" aria-labelledby="heading{}" data-bs-parent="#accordion">
                        <div class="accordion-body">
                            {}
                        </div>
                    </div>
                </div>
              '''.format(
                    i,
                    eclass(d),
                    i,
                    i,
                    args.backgroundcolor,
                    fixname(d),
                    i,
                    i,
                    formatdir(os.path.join(fromdir, d), basedir)
                    ))
            i += 1
        else:
            uncategorised.append(d)
            make_search_entry(os.path.join(fromdir, d), basedir)
    listfiletext += '</div>\n'

    if len(uncategorised) > 0:
        print("uncategorised:", uncategorised)
        for entry in uncategorised:
            listfiletext += formatfilelink(fromdir, entry, basedir, 0)

    with open(os.path.join(basedir, listfile), 'w') as o:
        o.write(listfiletext)
    print('list made in {}'.format(os.path.join(basedir, listfile)))

#-----------------------------
# DETECT CHANGES AND STOP IF NOTHING HAS CHANGED

if not os.path.exists(changelog):
    if args.override_changes:
        with open(changelog,"w") as o:
            o.write("{}")
    else:
        print ("no changelog file found at: {}\n Aborting makelist.\n".format(changelog))
        sys.exit()
new_changes_present=False
with open(changelog) as f:
    changes = json.load(f)
newtext = "\n<hr><h3>{:%d/%m/%Y %H:%M:%S}</h3>".format(datetime.now())
for thistype in changes:
    typechanges = [x for x in changes[thistype] if gl.accept(os.path.join(args.dir, x), os.path.split(x)[-1])]
    if len(typechanges) > 0:
        new_changes_present = True
        newtext += "<br>\n<h4>{}</h4>\n".format(thistype)
        for file in typechanges:
            newtext += "<p>{}</p>".format(changes[thistype][file].replace('\\',''))
oldtext = ""
if new_changes_present == True or args.override_changes:
    print ("New changes found. Making new search index.")
    with open(os.path.join(args.dir, gl.gofilename),"w") as o:
        o.write("go")
    if os.path.exists(changes_record_file):
        with open(changes_record_file) as f:
            oldtext = f.read()
    with open(changes_record_file,"w") as o:
        o.write(newtext + oldtext)
    with open(changelog,"w") as o:
        json.dump({},o)
else:
    print ("No new changes found in {}\n Aborting makelist.\n".format(changelog))
    with open(os.path.join(args.dir, gl.gofilename),"w") as o:
        o.write("no go")
    sys.exit()
#-----------------------------
if args.do_emergency:
    args.pin_to_top.append(args.emergencydirname)
    # Make and populate emergency folder
    # https://codepen.io/marklsanders/pen/OPZXXv
    emergencydir = os.path.join(guidelinesdir, args.emergencydirname)
    if not os.path.exists(emergencydir):
        os.mkdir(emergencydir)
    # clear emergencies
    for filename in os.listdir(emergencydir):
        cmd = 'rm "{}"'.format(os.path.join(emergencydir,filename))
        print (cmd)
        subprocess.call(cmd, shell=True)
    # copy emergencies
    for root, dirs, files in os.walk(args.dir):
       for name in files:
            if eclass(name)=="emergency":
                cmd = 'cp "{}" "{}"'.format(
                    os.path.join(root, name),
                    emergencydir
                    )
                print (cmd)
                subprocess.call(cmd, shell=True)

# load manually-set synonyms
gsyn = []
if os.path.exists(globalsynonymsfile):
    with open(globalsynonymsfile) as f:
        try:
            gsyn = json.load(f)
        except:
            print ("\n\n**** Misformatted GLOBAL SYNONYMS json file ****: {}\nIgnoring...\n\n".format(globalsynonymsfile))
else:
    with open(globalsynonymsfile,"w") as o:
        o.write("{}")

# Make html accordion menu and new search index
makelist(fromdir=guidelinesdir)

# Make and populate public folder
if os.path.exists(publicdir):
    # clear public folder
    for folder in os.listdir(publicdir):
        cmd = 'rm -r "{}"'.format(os.path.join(publicdir,folder))
        print (cmd)
        subprocess.call(cmd, shell=True)
else:
    os.mkdir(publicdir)
# copy publicfiles
publicguidelinesdir = os.path.join(publicdir, args.guidelinesdirname)
shutil.copytree(guidelinesdir, publicguidelinesdir, symlinks=False, ignore=ignore_files, ignore_dangling_symlinks=False, dirs_exist_ok=True)
makelist(fromdir=publicguidelinesdir)






















