#!/usr/bin/python3 -Es


import os
import sys
import argparse
import logging
import re
import json
from os.path import expanduser
from texttable import Texttable

base_dir = expanduser('~') + '/.config/mapt-repos'
cache_dir = expanduser('~') + '/.cache/mapt-repos'
aptconf = cache_dir + "/apt.conf"
if not os.path.isdir(cache_dir):
    os.makedirs(cache_dir, exist_ok=True)
with open(aptconf, "w") as fh:
    print('Dir "{}";'.format(cache_dir), file=fh)
os.environ["APT_CONFIG"] = aptconf


logger = logging.getLogger(__name__)

from mapt.repository import Repository
class Mapt:
    def __init__(self,suites):
        global base_dir
        self.suites=suites
        self.base_dir=base_dir
        
       
    def search(self,pkgname):
        print(os.environ["APT_CONFIG"])
        table = Texttable()
        data=[["Package", "Version","Suite","Arch"]]
        for suite in self.suites:
            if "skip" in suite:
                if suite["skip"]:
                    continue
            repo=Repository(self.base_dir,suite)
            d=repo.scan(pkgname)
            data=data+d
            
        table.add_rows(data)
        print(table.draw())
        
        
    

