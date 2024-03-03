#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re
import sys
import fitz
import timeit
import pandas as pd
from datetime import datetime
from dateutil.parser import parse
from itertools import product
import requests
from requests.exceptions import RequestException, Timeout, TooManyRedirects, URLRequired

#-----------------------------
import guideline_functions as gl
#-----------------------------
import argparse
parser = argparse.ArgumentParser()
parser.add_argument('-d', '--dir', default='lothiancriticalcare/1a74f8f7b8b7e871b413c4697f68b4401fbacdf0/') # default test dir
parser.add_argument('-r', '--reviewdatestrings',    action='append', default=['Next review', 'Review date', 'Review '], help='use this to append as many values as you want')
parser.add_argument('-v', '--verbose',    action="store_true", default=False,    help='increases verbosity')
parser.add_argument('-o', '--override_changes', default=False, action="store_true")
args = parser.parse_args()
#-----------------------------
if args.dir == "no_dir_specified":
    print ("no_dir_specified")
    sys.exit()
#-----------------------------

rs = [x.lower() for x in args.reviewdatestrings]
revout = os.path.join(args.dir,"reviewdates.csv")
revoutx = os.path.join(args.dir,"reviewdates.xlsx")
revout_big = os.path.join(args.dir,"reviewdates_full.csv")
changes_record_file = os.path.join(args.dir,"../changes.html")

linkout = os.path.join(args.dir,"linkchecks.csv")

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

def remove_spaces_from_urls(match):
    return match.group(0).replace(' ', '').replace('\n', '')

def find_urls(text):
    urlstem = r'http[s]?:\/\/[\S\s]{0,120}\/'
    url_pattern = re.compile(urlstem + r'[\S\s]{0,250}')
    endings = urlstem + r'[\S\s]*?(?:\.docx|\.doc|\.xlsx|\.pdf|\.html|\.htm|\.asp|\/$|\/\n|\/ )'
    urls = re.findall(url_pattern, text)
    output = []
    for url in urls:
        matches = list(re.finditer(r'http[s]?:\/\/', url))
        if len(matches) > 1:
            second_match_start = matches[1].start()
            url = url[:second_match_start]
        url = re.sub(urlstem, remove_spaces_from_urls, url)
        matches = re.findall(endings, url)
        if len(matches) > 0:
            url = matches[0]
        for terminator in [",",";"]:
            url = url.split(terminator)[0]
        url = url.strip().rstrip(".")
        output.append(url)
    return output

def get_base_url(url):
    base_url_regex = r'http[s]?:\/\/?(?:www\.)?[^\/:]+'
    match = re.findall(base_url_regex, url)
    if match:
        return match[0]
    else:
        return None

def check_url(url):
    # check local files first
    for stem in ["https://critcare.net/"+args.dir]:
        if url.startswith(stem):
            path = url.replace(stem,"")
            path = os.path.join(args.dir, path)
            if args.verbose:
                print ("testing filepath:", path)
            if os.path.exists(path):
                return 200
    # otherwise, check online
    if sum([url.startswith(stem) for stem in config["ignore_urls"]]) > 0:
        return "URL stem in ignorelist"
    try:
        response = requests.head(url, timeout=5)
        return response.status_code
    except Timeout:
        return "Request timed out."
    except TooManyRedirects:
        return "Too many redirects."
    except URLRequired:
        return "A valid URL is required."
    except RequestException as e:
        return f"An error occurred: {e}"
    except Exception as e:
        return f"An unexpected error occurred: {e}"
    return None


def response_acceptable(responsecode):
    if (str(responsecode).startswith("2") or str(responsecode).startswith("3")) and len(str(responsecode)) == 3:
        return True
    else:
        return False

def fix_url(input_url, max_tries=8):
    url_parts = input_url.replace('\n',' ').split(' ')
    if len(url_parts) > 5:
        return None
    space_combinations = list(product(["TRUNCATE", ""], repeat=len(url_parts) - 1))
    for i, combination in enumerate(space_combinations):
        url = ""
        for part, repl in zip(url_parts, combination + ("",)):
            if repl == "TRUNCATE":
                url += part
                break
            url += part + repl
        url = url.rstrip('.')
        response = check_url(url)
        if args.verbose:
            print (url, response)
        if response_acceptable(response):
            return url
    return None

def extract_hyperlinks(file_path):
    doc = fitz.open(file_path)
    hyperlinks = []

    for page in doc:
        links = page.get_links()
        for link in links:
            if link['kind'] == 2:  # External URI
                hyperlinks.append(link['uri'])

    return hyperlinks


if not (gl.newchanges(args.dir) or args.override_changes):
    print ("Stopping because go file is no-go.")
    sys.exit()

revs = {}
links = {}
for dirpath, _, filenames in os.walk(args.dir):
    for filename in filenames:
        if filename.lower().endswith('.pdf'):
            file_path = os.path.join(dirpath, filename)
            if not gl.is_reportable(file_path):
                continue
            cleanpath = gl.shorten_filepath(file_path).replace(",","")
            links[cleanpath]=[]
            text = gl.readfilecontents(file_path)
            if text:
                text = text.replace("\r","\n")
                lines = text.lower().split("\n")+["."]
                # GET REVIEW LINES
                reviewlines = []
                for r in rs:
                    reviewlines += [x.strip()+" "+lines[i+1].strip() for i,x in enumerate(lines[:-1]) if r in x]
                reviewdates = []
                for x in reviewlines:
                    d = extract_date(x)
                    if d:
                        if args.verbose and False:
                            print("{:<20}\t<==\t{}".format(d.strftime('%Y-%m-%d %H:%M:%S'),x))
                        reviewdates.append(d)
                if len(reviewdates)>0:
                    revs[cleanpath] = [max(reviewdates), " | ".join(reviewlines)]
                # GET LINK LINES
                true_links = extract_hyperlinks(file_path)
                for link in true_links:
                    links[cleanpath].append([link, response_acceptable(check_url(link))])
                possible_links = find_urls(text)
                for link in possible_links: 
                    fixedlink = fix_url(link)
                    if fixedlink:
                        links[cleanpath].append([fixedlink, True])
                    else:
                        links[cleanpath].append([link.replace("\n",""), False])

data_list = [{'File': key, 'Review date': val[0], 'Source string': val[1]} for key, val in revs.items()]
df = pd.DataFrame(data_list)
if (len(df)>0):
    df['Review date'] = pd.to_datetime(df['Review date'], errors='coerce')
    df.dropna(subset=['Review date'], inplace=True)
    df.sort_values('Review date', ascending=True, inplace=True)
    df['Review date'] = df['Review date'].dt.strftime('%Y-%m-%d')
    df = df.dropna(how='all')
    df[["File", "Review date"]].to_csv(revout, index=False)
    df[["File", "Review date"]].to_excel(revoutx, index=False)
df.to_csv(revout_big, index=False)

with open(linkout, "w") as o:
    for cleanpath in sorted(links):
        for link in links[cleanpath]:
            o.write(f"{cleanpath},{link[0]},{link[1]}\n")







