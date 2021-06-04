#!/usr/bin/env python3

'''
Makes an html list of pdf files in a directory
Also makes a lunr search index
'''
import re
import os
import sys
import json
import shutil
import subprocess
from io import StringIO
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
#-----------------------------
scriptpath = os.path.dirname(os.path.realpath(__file__))
#-----------------------------
import argparse
parser = argparse.ArgumentParser()
parser.add_argument('-d', '--dir', default=os.path.join(scriptpath,'../docs/test_secret/criticalcare/'))
parser.add_argument('-p', '--publicdir', default=os.path.join(scriptpath,'../docs/test_pub/criticalcare/'))
parser.add_argument('-l', '--listfilename', default='list.html')
parser.add_argument('-i', '--indexfilename', default='index.json')
parser.add_argument('-f', '--fast', default=False, action="store_true")
args = parser.parse_args()
#-----------------------------
use_viewerjs = False
emergencydir = "Emergencies" # this will be pinned to the top and copies of emergency protocols uploaded to it
excluded = ['Icon']
pin_to_top = [emergencydir]
#-----------------------------

def convert_pdf_to_txt(thisfile):
    rsrcmgr = PDFResourceManager()
    retstr = StringIO()
    codec = 'utf-8'  # 'utf16','utf-8'
    laparams = LAParams()
    device = TextConverter(rsrcmgr, retstr, laparams=laparams)
    fp = open(thisfile, 'rb')
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    password = ""
    maxpages = 0
    caching = True
    pagenos = set()
    for page in PDFPage.get_pages(fp, pagenos, maxpages=maxpages, password=password, caching=caching, check_extractable=True):
        interpreter.process_page(page)
    fp.close()
    device.close()
    str = retstr.getvalue()
    retstr.close()
    return str

def readpdf(thisfile):
    if not thisfile.endswith(".pdf"):
        return ""
    try:
        return convert_pdf_to_txt(thisfile)
    except Exception as e:
        print ("failed to convert to pdf:", thisfile)
        print(e)
        return ""

def get_unique_words(bigstring):
    deletelist = ['\ufb01','\u00e2','\u2021','\u2013','\ufb02','\ufb02','\ufb00','-','\u201c','\u201d']
    for char in deletelist:
        bigstring = bigstring.replace(char,'')
    for char in ['\t','.','[',']','(',')','{','}','"',"'"]:
        bigstring = bigstring.replace(char,' ')
    bs = [x.strip() for x in re.split(';| |,|\n|\r',bigstring)]
    bs = list(set([x for x in bs if len(x)>1]))
    return ' '.join(bs)

def add_pdf_to_search(thisfile, thisbasedir, already):
    if not args.fast:
        thistitle = fixname(os.path.split(thisfile)[1])
        alreadydic={}
        for x in already:
            try:
                if x['title'] == thistitle:
                    return
            except:
                continue
        return {
            'href': os.path.relpath(thisfile, thisbasedir),
            'title': thistitle,
            'content': get_unique_words(readpdf(thisfile)), # this is the slow bit
            }

def accept(thispath, file_or_dir_name):
    if file_or_dir_name.startswith('.') or file_or_dir_name.startswith('offline') or file_or_dir_name.startswith('_'):
        return False
    if file_or_dir_name.strip() in excluded:
        return False
    dirpath = os.path.join(thispath, file_or_dir_name)
    if os.path.isdir(dirpath):
        acceptable = [x for x in os.listdir(dirpath) if accept(dirpath, x)]
        if len(acceptable) == 0:
            return False
    return True

def eclass(filename):
    emlabels = ["_em.", "_em_", "Emergency", "emergency", "Emergencies"]
    for x in emlabels:
        if x in filename:
            return "emergency"
    return ""

def is_public(filepath):
    thispath, filename = os.path.split(filepath)
    if not(accept(thispath, filename)):
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

def formatdir(thisdir, basedir, sl, depth=0):
    text = ''
    for entry in sorted(os.listdir(thisdir)):
        if not accept(thisdir, entry):
            continue
        if os.path.isdir(os.path.join(thisdir, entry)):
            text+=('''
                <div class='panel-group' id='{}'>
                    <div class='panel'>
                        <h5 style='margin-left:{}em;'>
                            <a class='{}' data-toggle='collapse' data-parent='#{}' href='#collapse{}'>
                                {} &raquo;
                            </a>
                        </h5>
                        <div id="collapse{}" class="panel-collapse collapse">
                            <ul class='list-group'>{}</ul>
                        </div>
                    </div>
                </div>
                '''.format(
                        makeid(entry),
                        depth+1,
                        eclass(entry),
                        makeid(entry),
                        makeid(entry),
                        fixname(entry),
                        makeid(entry),
                        formatdir(os.path.join(thisdir, entry), basedir, sl, depth+1)
                        )
                    )
        else:
            if accept(thisdir, entry):
                if entry.endswith('.txt'):
                    print ("h:", entry)
                    with open(os.path.join(thisdir,entry)) as f:
                        filecontents = f.read()
                    text+=('''
                        <a class='{}' href='{}'>
                            <li class='list-group-item' style='margin-left:{}em;'>{}</li>
                        </a>
                        '''.format(
                            eclass(entry),
                            filecontents,
                            depth,
                            fixname(entry))
                            )
                elif use_viewerjs:
                    text+=('''
                        <a class='{}' href='ViewerJS/#../{}'>
                            <li class='list-group-item' style='margin-left:{}em;'>{}</li>
                        </a>
                        '''.format(
                            eclass(entry),
                            os.path.relpath(os.path.join(thisdir, entry), basedir),
                            depth,
                            fixname(entry))
                            )
                else:
                    text+=('''
                        <a class='{}' href='{}'>
                            <li class='list-group-item' style='margin-left:{}em;'>{}</li>
                        </a>
                        '''.format(
                            eclass(entry),
                            os.path.relpath(os.path.join(thisdir, entry), basedir),
                            depth,
                            fixname(entry))
                            )
                sl.append(add_pdf_to_search(os.path.join(thisdir, entry), basedir, sl))
    return text


def makelist(fromdir=args.dir, listfile=args.listfilename, indexfile=args.indexfilename):
    i=0
    basedir = os.path.abspath(os.path.join(fromdir,"..")) # always one level up, by definition because of the links
    searchlist = []
    uncategorised = []
    listfiletext = ""
    listfiletext += ('<div class="panel-group" id="accordion" role="tablist" aria-multiselectable="true">\n')
    topdirlist = [x for x in sorted(os.listdir(fromdir)) if x not in pin_to_top]
    topdirlist = pin_to_top + topdirlist
    for d in topdirlist:
        if not(accept(fromdir, d)):
            continue
        if os.path.isdir(os.path.join(fromdir, d)):
            listfiletext += ('''
                <div class="panel panel-default">
                    <a role="button" class="{}" data-toggle="collapse" data-parent="#accordion" href="#collapse{}" aria-expanded="true" aria-controls="collapse{}">
                        <div class="panel-heading" role="tab" id="heading{}" style="background: #f5f5f5;">
                            <h4 class="panel-title">
                              {}
                            </h4>
                        </div>
                    </a>
                    <div id="collapse{}" class="panel-collapse collapse" role="tabpanel" aria-labelledby="heading{}">
                            {}
                    </div>
                </div>
              '''.format(
                    eclass(d),
                    i,
                    i,
                    i,
                    fixname(d),
                    i,
                    i,
                    formatdir(os.path.join(fromdir, d), basedir, searchlist)
                    ))
            i+=1
        else:
            if accept(fromdir, d):
                uncategorised.append(d)
                searchlist.append(add_pdf_to_search(os.path.join(fromdir, d), basedir, searchlist))
    listfiletext += ('</div>\n')

    if len(uncategorised)>0:
        print (uncategorised)
        listfiletext += ("<div class='panel panel-default' style='margin-top:1em;'><ul class='list-group'>\n")
        for entry in uncategorised:
            if accept(fromdir, entry):
                listfiletext += (("\t<a class='{}' href='{}'><li class='list-group-item'>{}</li></a>\n".format(eclass(entry), os.path.relpath(os.path.join(fromdir, entry), basedir), fixname(entry))))
                searchlist.append(add_pdf_to_search(os.path.join(fromdir, entry), basedir, searchlist))
        listfiletext += ('</ul></div>\n')

    with open(os.path.join(basedir,listfile),'w') as o:
        o.write(listfiletext)

    if not args.fast:
        with open(os.path.join(basedir,indexfile),'w') as o:
            json.dump(searchlist, o, indent=4)

    print ('list made in {}'.format(os.path.join(basedir,listfile)))
    # check for duplicate filenames:
    allfiles={}
    for root, dirs, files in os.walk(fromdir):
        for name in files:
            if accept(root,name):
                if emergencydir not in root and ".temp" not in root:
                    try:
                        allfiles[name]
                        print ("\n******\nDuplicate filename found:\n\t{}\n\t{}\n".format(
                                os.path.join(root, name),
                                allfiles[name]
                            ))
                    except:
                        pass
                    allfiles[name]=os.path.join(root,name)

#-----------------------------

# https://codepen.io/marklsanders/pen/OPZXXv

edir = os.path.join(args.dir, emergencydir)
if not os.path.exists(edir):
    os.mkdir(edir)
# clear emergencies
for filename in os.listdir(edir):
    cmd = 'rm "{}"'.format(os.path.join(edir,filename))
    print (cmd)
    subprocess.call(cmd, shell=True)
# copy emergencies
for root, dirs, files in os.walk(args.dir):
   for name in files:
        if eclass(name)=="emergency":
            cmd = 'cp "{}" "{}"'.format(
                os.path.join(root, name),
                edir
                )
            print (cmd)
            subprocess.call(cmd, shell=True)
makelist()

if os.path.exists(args.publicdir):
    # clear public folder
    for folder in os.listdir(args.publicdir):
        cmd = 'rm -r "{}"'.format(os.path.join(args.publicdir,folder))
        print (cmd)
        subprocess.call(cmd, shell=True)
else:
    os.mkdir(args.publicdir)
# copy publicfiles
shutil.copytree(args.dir, args.publicdir, symlinks=False, ignore=ignore_files, ignore_dangling_symlinks=False, dirs_exist_ok=True)
makelist(fromdir=args.publicdir)






