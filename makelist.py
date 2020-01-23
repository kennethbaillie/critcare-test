#!/usr/bin/env python3

'''
Makes an html list of pdf files in a directory
Also makes a lunr search index
'''
import re
import os
import sys
import json
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
parser.add_argument('-d', '--dir', default=os.path.join(scriptpath,'docs/criticalcare/'))
parser.add_argument('-o', '--outputfile', default=os.path.join(scriptpath,'docs/list.html'))
parser.add_argument('-i', '--indexfile', default=os.path.join(scriptpath,'docs/index.json'))
parser.add_argument('-b', '--basedir', default=os.path.join(scriptpath,'docs'))
parser.add_argument('-f', '--fast', default=False, action="store_true")
args = parser.parse_args()
#-----------------------------
use_viewerjs = False
excluded = ['Icon']
pin_to_top = ['Emergencies']
#-----------------------------

def convert_pdf_to_txt(thisfile):
    rsrcmgr = PDFResourceManager()
    retstr = StringIO()
    codec = 'utf-8'  # 'utf16','utf-8'
    laparams = LAParams()
    device = TextConverter(rsrcmgr, retstr, codec=codec, laparams=laparams)
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
    try:
        return convert_pdf_to_txt(thisfile)
    except:
        return ""

def get_unique_words(bigstring):
    for char in ['\ufb01','\u00e2','\u2021','\u2013','\ufb02','\ufb02','\ufb00','-']:
        bigstring = bigstring.replace(char,'')
    for char in ['\t','.','[',']','(',')','{','}','"',"'"]:
        bigstring = bigstring.replace(char,' ')
    bs = [x.strip() for x in re.split(';| |,|\n|\r',bigstring)]
    bs = list(set([x for x in bs if len(x)>1]))
    return ' '.join(bs)

def add_pdf_to_search(thisfile):
    if not args.fast:
        searchlist.append({
            'href': os.path.relpath(thisfile, args.basedir),
            'title': fixname(os.path.split(thisfile)[1]),
            'content': get_unique_words(readpdf(thisfile)), # this is the slow bit
            })

def accept(filename):
    if filename.startswith('.') or filename.startswith('offline'):
        return False
    if filename.strip() in excluded:
        return False
    return True

def fixname(thisname):
    return thisname.replace("_"," ").split('.')[0]

def makeid(thisname):
    return ''.join(thisname.split())

def formatdir(thisdir, depth=0):
    text = ''
    for entry in os.listdir(thisdir):
        if os.path.isdir(os.path.join(thisdir, entry)):
            #text+=("<h5 style='margin-left:{}em;'>{}:</h5><ul class='list-group'>\n{}\n</ul>\n".format(depth+1, fixname(entry), formatdir(os.path.join(thisdir, entry), depth+1)))
            text+=('''
                <div class='panel-group' id='{}'>
                    <div class='panel'>
                        <h5 style='margin-left:{}em;'>
                            <a data-toggle='collapse' data-parent='#{}' href='#collapse{}'>
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
                        makeid(entry),
                        makeid(entry),
                        fixname(entry),
                        makeid(entry),
                        formatdir(os.path.join(thisdir, entry), depth+1))
                        )

        else:
            if accept(entry):
                if use_viewerjs:
                    text+=('''
                        <a href='ViewerJS/#../{}'>
                            <li class='list-group-item' style='margin-left:{}em;'>{}</li>
                        </a>
                        '''.format(
                            os.path.relpath(os.path.join(thisdir, entry), args.basedir),
                            depth,
                            fixname(entry))
                            )
                else:
                    text+=('''
                        <a href='{}'>
                            <li class='list-group-item' style='margin-left:{}em;'>{}</li>
                        </a>
                        '''.format(
                            os.path.relpath(os.path.join(thisdir, entry), args.basedir),
                            depth,
                            fixname(entry))
                            )
                add_pdf_to_search(os.path.join(thisdir, entry))
    return text
#-----------------------------

# https://codepen.io/marklsanders/pen/OPZXXv


searchlist = []

outfiletext = ""
outfiletext += ('<div class="panel-group" id="accordion" role="tablist" aria-multiselectable="true">\n')
i=0
uncategorised = []
topdirlist = pin_to_top + [x for x in sorted(os.listdir(args.dir)) if x not in pin_to_top]
for d in topdirlist:
    if os.path.isdir(os.path.join(args.dir, d)):
        outfiletext += ('''
            <div class="panel panel-default">
                <a role="button" data-toggle="collapse" data-parent="#accordion" href="#collapse{}" aria-expanded="true" aria-controls="collapse{}">
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
                i,
                i,
                i,
                fixname(d),
                i,
                i,
                formatdir(os.path.join(args.dir, d))
                ))
        i+=1
    else:
        if os.path.exists(os.path.join(args.dir, d)) and accept(d):
            uncategorised.append(d)
            add_pdf_to_search(os.path.join(args.dir, d))
outfiletext += ('</div>\n')

if len(uncategorised)>0:
    print (uncategorised)
    o.write("<div class='panel panel-default' style='margin-top:1em;'><ul class='list-group'>\n")
    for entry in uncategorised:
        if accept(entry):
            o.write(("\t<a href='{}'><li class='list-group-item'>{}</li></a>\n".format(os.path.relpath(os.path.join(args.dir, entry), args.basedir), fixname(entry))))
            add_pdf_to_search(os.path.join(args.dir, entry))
    o.write('</ul></div>\n')


with open(args.outputfile,'w') as o:
    o.write(outfiletext)

if not args.fast:
    with open(args.indexfile,'w') as o:
        json.dump(searchlist, o, indent=4)

print ('list made')


