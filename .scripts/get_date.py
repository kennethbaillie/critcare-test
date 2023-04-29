#!/usr/bin/env python3

import os
import timeit
import pandas as pd
#-----------------------------
import guideline_functions as gl
#-----------------------------
import argparse
parser = argparse.ArgumentParser()
parser.add_argument('-s', '--sourcedir', default='docs/test_secret') # default test dir
parser.add_argument('-r', '--reviewdatestrings',    action='append', default=['Next review', 'Review Date'], help='use this to append as many values as you want')
parser.add_argument('-v', '--verbose',    action="store_true", default=False,    help='increases verbosity')
args = parser.parse_args()
#-----------------------------
if args.sourcedir == "no_dir_specified":
    print ("no_dir_specified")
    sys.exit()
#-----------------------------

rs = [x.lower() for x in args.reviewdatestrings]
revout = os.path.join(args.sourcedir,"reviewdates.csv")

revs = {}
for dirpath, _, filenames in os.walk(args.sourcedir):
    for filename in filenames:
        if filename.lower().endswith('.pdf'):
            file_path = os.path.join(dirpath, filename)
            text = gl.get_pdf_text(file_path)
            if text:
                text = text.replace("\r","\n")
                lines = text.lower().split("\n")+["."]
                reviewlines = []
                for r in rs:
                    reviewlines += [x.strip()+" "+lines[i+1].strip() for i,x in enumerate(lines[:-1]) if r in x]
                if len(reviewlines)>0:
                    revs[file_path] = reviewlines[0]

df = pd.DataFrame(list(revs.items()), columns=["path", "content"])
df.to_csv(revout)


