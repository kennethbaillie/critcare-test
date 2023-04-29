#!/usr/bin/env python3

import os
import sys
import json
import shutil
import pathlib
import filecmp
from zipfile import ZipFile
from io import StringIO
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
import PyPDF2

#-----------------------------
# files to ignore
ignorelist = [
        "temp.zip",
        ".DS_Store",
        ".temp",
        "temp",
        ".changes.json",
        "duplicates.md",
        "changes.html",
        "__MACOSX",
        "offline_DRAFTS",
        'Icon'
    ]

exclude_from_reports = [
    "Emergencies",
]


class cd:
    """Context manager for changing the current working directory"""
    """ by Brian M. Hunt https://stackoverflow.com/users/19212/brian-m-hunt"""
    def __init__(self, newPath):
        self.newPath = os.path.expanduser(newPath)

    def __enter__(self):
        self.savedPath = os.getcwd()
        os.chdir(self.newPath)

    def __exit__(self, etype, value, traceback):
        os.chdir(self.savedPath)


def accept(thispath, file_or_dir_name):
    if file_or_dir_name.startswith('.') or file_or_dir_name.startswith('offline') or file_or_dir_name.startswith('_') or "_bak." in file_or_dir_name:
        return False
    if file_or_dir_name.strip() in ignorelist:
        return False
    dirpath = os.path.join(thispath, file_or_dir_name)
    if os.path.isdir(dirpath):
        acceptable = [x for x in os.listdir(dirpath) if accept(dirpath, x)]
        if len(acceptable) == 0:
            return False
    return True


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

def readfilecontents(thisfile):
    if thisfile.endswith(".pdf"):
        try:
            return convert_pdf_to_txt(thisfile)
        except Exception as e:
            print ("failed to convert to txt:", thisfile)
            print(e)
            return ""
    else:
        try:
            with open(thisfile) as f:
                text = f.read()
                return get_unique_words(text)
        except Exception as e:
            print ("failed to read file:", thisfile)
            print(e)
            return ""

def get_pdf_text(file_path):
    try:
        with open(file_path, 'rb') as f:
            pdf_reader = PyPDF2.PdfFileReader(f, strict=False)
            text = ''
            for page_num in range(pdf_reader.numPages):
                text += pdf_reader.getPage(page_num).extractText()
            return text
    except Exception as e:
        #print(f"Error processing {file_path}: {e}")
        return None

def recursive_split(s):
    stem, name = list(os.path.split(s))
    if stem in ['', os.path.sep]:
        return [name]
    return recursive_split(stem) + [name]

def is_reportable(thispath, verbose=True):
    dir_and_file_names = recursive_split(thispath)
    if "." in dir_and_file_names:
        dir_and_file_names.remove('.')
    for name in dir_and_file_names:
        if not accept("", name):
            return False
        if name in ignorelist+exclude_from_reports:
            return False
    return True

def shorten_filepath(thispath, dirs_to_remove=3):
    dirs = thispath.split(os.path.sep)
    new_dirs = dirs[dirs_to_remove:]
    return os.path.join(*new_dirs)



