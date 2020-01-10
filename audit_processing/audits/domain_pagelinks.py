import sys
import requests
import os
import json
from requests.exceptions import ConnectionError

url = sys.argv[1]

resp = requests.get(f'http://api.hackertarget.com/pagelinks/?q={url}').text
resp = resp.splitlines()
error_codes = [400, 404, 403, 408, 409, 501, 502, 503]
links = []
for line in resp:
    if line.count('http://') > 1:
        tmp = line.split('http://')
        tmp = ['http://'+el for el in tmp if el]
    elif line.count('https://') > 1:
        tmp = line.split('https://')
        tmp = ['https://' + el for el in tmp if el]
    elif line.count('https://') == 0 and line.count('http://') == 0:
        tmp = []
    else:
        tmp = [line]
    for link in tmp:
        try:
            code = requests.get(link).status_code
            if code not in error_codes:
                links.append({
                    'link': link
                })
        except ConnectionError:
            continue
basepath = os.path.dirname(__file__)
filepath = os.path.abspath(os.path.join(basepath, "..", "output", "domain_pagelinks.json"))
with open(filepath, 'w') as f:
    json.dump(links, f)