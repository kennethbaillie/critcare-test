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
revoutx = os.path.join(args.sourcedir,"../","reviewdates.xlsx")
revout_big = os.path.join(args.sourcedir,"../","reviewdates_full.csv")
changes_record_file = os.path.join(args.sourcedir,"../changes.html")

def old_extract_date(text, reviewstrings=rs):
    while "  " in text:
        text = text.replace("  "," ")
    text = text.replace(" :",":")
    for phrase in reviewstrings:
        idx = text.find(phrase)
        if idx != -1:
            date_str = text[idx + len(phrase):idx + len(phrase)+22].strip()
            time_related_words = ['hours', 'minutes', 'seconds']
            pattern = re.compile(r'\b(?:{})\b'.format('|'.join(time_related_words)), re.IGNORECASE)
            date_str = pattern.sub('', date_str)
            print (date_str)
            date_match = re.search(r'\d{1,2}[/-]\d{1,2}[/-]\d{2,4}', date_str)
            if date_match:
                return parse(date_match.group(0), dayfirst=True)
            else:
                words = date_str.split()
                for i, word in enumerate(words):
                    if word.isdigit() and 1 <= int(word) <= 12:
                        try:
                            return parse(f'{word} {words[i + 1]}', fuzzy=True, yearfirst=True)
                        except:
                            pass
                    elif re.match(r'[a-zA-Z]+', word):
                        try:
                            return parse(f'{word} {words[i + 1]}', fuzzy=True, yearfirst=True)
                        except:
                            pass
    return None

def extract_date(s):
    s = s.replace(" :",": ")
    while "  " in s:
        s = s.replace("  "," ")
    months = ['january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october', 'november', 'december']
    months += [x[:3] for x in months]

    # Remove any words related to time using a regular expression
    time_related_words = ['hours', 'minutes', 'seconds']
    pattern = re.compile(r'\b(?:{})\b'.format('|'.join(time_related_words)), re.IGNORECASE)
    s_cleaned = pattern.sub('', s)
    s_cleaned = re.sub(r'(?<=20)(\d)\s(\d)', r'\1\2', s_cleaned)

    # Insert a space before a month name if it's immediately preceded by a digit
    for month in months:
        s_cleaned = re.sub(r'(\d)(' + month + ')', r'\1 \2', s_cleaned, flags=re.IGNORECASE)

    # Insert a space before a digit if it's immediately preceded by a month name
    for month in months:
        s_cleaned = re.sub(r'(' + month + r')(\d)', r'\1 \2', s_cleaned, flags=re.IGNORECASE)

    words = s_cleaned.split()

    dates = []
    for i, word in enumerate(words):
        if word.lower() in months:
            try:
                # Attempt to parse the date using dateutil
                date_string = f"{words[i]} {words[i + 1]}"
                parsed_date = parse(date_string, fuzzy=True, yearfirst=True)
                dates.append(parsed_date)
            except (ValueError, IndexError):
                continue
    if len(dates)>0:
        return(max(dates))
    else:
        return None

if not gl.newchanges(changes_record_file):
    print ("Stopping because {} hasn't changed.".format(changes_record_file))
    sys.exit()

revs = {}
for dirpath, _, filenames in os.walk(args.sourcedir):
    for filename in filenames:
        if filename.lower().endswith('.pdf'):
            file_path = os.path.join(dirpath, filename)
            if not gl.is_reportable(file_path):
                continue
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
                    revs[gl.shorten_filepath(file_path).replace(",","")] = [max(reviewdates), " | ".join(reviewlines)]


data_list = [{'File': key, 'Review date': val[0], 'Source string': val[1]} for key, val in revs.items()]
df = pd.DataFrame(data_list)
#df = pd.DataFrame(list(revs.items()), columns=["File", "Review date"])
df = pd.concat([df, pd.DataFrame([{'File': '==TODAY==', 'Review date': datetime.today()}])], ignore_index=True)
df['Review date'] = pd.to_datetime(df['Review date'], errors='coerce')
df.dropna(subset=['Review date'], inplace=True)
df.sort_values('Review date', ascending=True, inplace=True)
df['Review date'] = df['Review date'].dt.strftime('%Y-%m-%d')
df[["File", "Review date"]].to_csv(revout, index=False)
df[["File", "Review date"]].to_excel(revoutx, index=False)
df.to_csv(revout_big, index=False)


