#!/usr/bin/python3 -Es
import mapt
import sys
import json
import os



if len(sys.argv) !=2:
    print("Usage - ./run [package name]")
    exit()
  
if __name__ == "__main__":
    suites=None
    with open('suites.json') as f:
        suites= json.load(f)
    m=mapt.Mapt(suites)
    m.search(sys.argv[1])
    