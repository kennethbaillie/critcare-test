#!/usr/bin/env python3

import os
import timeit
import pandas as pd
import re
from datetime import datetime
from dateutil.parser import parse
#-----------------------------
import guideline_functions as gl
#-----------------------------
import argparse
parser = argparse.ArgumentParser()
parser.add_argument('-s', '--sourcedir', default='docs/test_secret') # default test dir
parser.add_argument('-r', '--reviewdatestrings',    action='append', default=['Next review', 'Review date', 'Review '], help='use this to append as many values as you want')
parser.add_argument('-v', '--verbose',    action="store_true", default=False,    help='increases verbosity')
args = parser.parse_args()
#-----------------------------
if args.sourcedir == "no_dir_specified":
    print ("no_dir_specified")
    sys.exit()
#-----------------------------

rs = [x.lower() for x in args.reviewdatestrings]
revout = os.path.join(args.sourcedir,"../","reviewdates.csv")
revout2 = os.path.join(args.sourcedir,"../","reviewdates_full.csv")

def extract_date(text, reviewstrings=rs):
    while "  " in text:
        text = text.replace("  "," ")
    text = text.replace(" :",":")
    for phrase in reviewstrings:
        idx = text.find(phrase)
        if idx != -1:
            date_str = text[idx + len(phrase):idx + len(phrase)+22].strip()
            date_match = re.search(r'\d{1,2}[/-]\d{1,2}[/-]\d{2,4}', date_str)
            if date_match:
                return parse(date_match.group(0), dayfirst=True)
            else:
                words = date_str.split()
                for i, word in enumerate(words):
                    if word.isdigit() and 1 <= int(word) <= 12:
                        try:
                            return parse(f'{word} {words[i + 1]}', yearfirst=True)
                        except:
                            pass
                    elif re.match(r'[a-zA-Z]+', word):
                        try:
                            return parse(f'{word} {words[i + 1]}', yearfirst=True)
                        except:
                            pass
    return None

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
                reviewdates = []
                for x in reviewlines:
                    d = extract_date(x)
                    if d:
                        print("{:<20}\t<==\t{}".format(d.strftime('%Y-%m-%d %H:%M:%S'),x))
                        reviewdates.append(d)

                if len(reviewdates)>0:
                    revs[file_path] = [max(reviewdates), " | ".join(reviewlines)]


data_list = [{'File': key, 'Review date': val[0], 'Source string': val[1]} for key, val in revs.items()]
df = pd.DataFrame(data_list)
#df = pd.DataFrame(list(revs.items()), columns=["File", "Review date"])
print (df)
df = df.append({'File': '==TODAY==', 'Review date': datetime.today()}, ignore_index=True)
df['Review date'] = pd.to_datetime(df['Review date'], errors='coerce')
df.dropna(subset=['Review date'], inplace=True)
df.sort_values('Review date', ascending=True, inplace=True)
df['Review date'] = df['Review date'].dt.strftime('%Y-%m-%d')
df[["File", "Review date"]].to_csv(revout, index=False)
df.to_csv(revout2, index=False)


