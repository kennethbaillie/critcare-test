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
        "changes.html",
        "__MACOSX",
        "offline_DRAFTS",
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


