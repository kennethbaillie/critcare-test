#!/usr/bin/env python3

import os
import sys
import json
import shutil
import pathlib
import filecmp
from zipfile import ZipFile

#-----------------------------
# files to ignore in comparison
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
        "Emergencies",
        'Icon'
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



    