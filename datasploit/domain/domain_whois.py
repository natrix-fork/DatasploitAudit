#!/usr/bin/env python
import os
import json
import base
import sys
import whois
from termcolor import colored
import time

ENABLED = True


class style:
    BOLD = '\033[1m'
    END = '\033[0m'


def whoisnew(domain):
	try:
	    w = whois.whois(domain)
	    return dict(w)
	except:
		return {}


def banner():
    print colored(style.BOLD + '---> Finding Whois Information.' + style.END, 'blue')


def main(domain):
    return whoisnew(domain)


def output(data, domain=""):
    for k in ('creation_date', 'expiration_date', 'updated_date'):
        if k in data:
            date = data[k][0] if isinstance(data[k], list) else data[k]
            if data[k]:
                data[k] = date.strftime('%m/%d/%Y')
    print data
    basepath = os.path.dirname(__file__)
    filepath = os.path.abspath(
        os.path.join(basepath, "..", "..", "audit_processing", "output", "domain_whois.json"))
    with open(filepath, 'w') as f:
        json.dump(data, f)
    print "\n-----------------------------\n"


if __name__ == "__main__":
    try:
        domain = sys.argv[1]
        banner()
        result = main(domain)
        output(result, domain)
    except Exception as e:
        print e
        print "Please provide a domain name as argument"
