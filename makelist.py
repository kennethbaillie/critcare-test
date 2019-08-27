#!/opt/local/bin/python
# -*- coding: UTF-8 -*-

'''
Makes an html list of pdf files in a directory
'''

import os
import sys
import json
#-----------------------------
scriptpath = os.path.dirname(os.path.realpath(__file__))
#-----------------------------
import argparse
parser = argparse.ArgumentParser()
parser.add_argument('-d', '--dir', default=os.path.join(scriptpath,'docs/pdfs/'))
parser.add_argument('-o', '--outputfile', default=os.path.join(scriptpath,'docs/list.html'))
parser.add_argument('-b', '--basedir', default=os.path.join(scriptpath,'docs'))
args = parser.parse_args()
#-----------------------------
def accept(filename):
    if filename.startswith('.'):
        return False
    return True

def fixname(thisname):
    return thisname.replace("_"," ")

def formatdir(thisdir):
    text = ''
    for entry in os.listdir(thisdir):
        if os.path.isdir(os.path.join(thisdir, entry)):
            text+=("<h6>{}</h6><ul class='list-group'>\n{}\n</ul>\n".format(fixname(entry), formatdir(os.path.join(thisdir, entry))))
        else:
            if accept(entry):
                text+=("\t<a href='{}'><li class='list-group-item'>{}</li></a>\n".format(os.path.relpath(os.path.join(thisdir, entry), args.basedir), fixname(entry)))
    return text

#-----------------------------
with open(args.outputfile,'w') as o:
    o.write('<div class="panel-group" id="accordion" role="tablist" aria-multiselectable="true">\n')
    divcount=0
    for d in os.listdir(args.dir):
        if os.path.isdir(os.path.join(args.dir, d)):
            o.write('''  <div class="panel panel-default">
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
  </div>'''.format(divcount, divcount, divcount, fixname(d), divcount, divcount, formatdir(os.path.join(args.dir, d)) ))
            divcount+=1
    o.write('</div>\n')







