import sys
import subprocess

domain = sys.argv[1]

result = subprocess.run(['../../datasploit/venv/bin/python2.7', '../../datasploit/domain/domain_censys.py', domain],
                        stdout=subprocess.PIPE).stdout.decode('utf-8')
print(result)
