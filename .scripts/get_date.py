#!/usr/bin/env python3

import os
import timeit
#-----------------------------
import guideline_functions as gl
#-----------------------------
import argparse
parser = argparse.ArgumentParser()
parser.add_argument('-s', '--sourcedir', default='docs/test_secret') # default test dir
parser.add_argument('-v', '--verbose',    action="store_true", default=False,    help='increases verbosity')
args = parser.parse_args()
#-----------------------------
if args.sourcedir == "no_dir_specified":
    print ("no_dir_specified")
    sys.exit()
#-----------------------------

t1 = []
t2 = []

for dirpath, _, filenames in os.walk(args.sourcedir):
    for filename in filenames:
        print (filename)
        if filename.lower().endswith('.pdf'):
            file_path = os.path.join(dirpath, filename)
            pdf_text1 = gl.get_pdf_text(file_path)
            pdf_text2 = gl.readfilecontents(file_path)

            t1.append(timeit.timeit(lambda: gl.get_pdf_text(file_path), number=1))
            t2.append(timeit.timeit(lambda: gl.readfilecontents(file_path), number=1))


print (t1)
print (t2)