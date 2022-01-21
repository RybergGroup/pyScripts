#! /usr/bin/python3

import requests
import sys

for i in range(1,len(sys.argv)):
    r = requests.get("http://api.crossref.org/works/" + sys.argv[i] + "/transform/application/x-bibtex")
    if r.status_code == 200:
        print(r.text)
    else:
        sys.stderr.write("Error getting BibTex for " + sys.argv[i])
