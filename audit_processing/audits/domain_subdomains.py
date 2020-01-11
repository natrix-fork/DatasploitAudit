import sys
import time
import os
import json


from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.keys import Keys


options = Options()
options.add_argument('--headless')

domain = sys.argv[1]
driver = Firefox('/usr/local/bin', options=options)
driver.get('https://dnsdumpster.com/')
time.sleep(5)
subdomains = []
try:
    form = driver.find_element_by_xpath('//input[@id="regularInput"]')
    form.send_keys(domain)
    time.sleep(2)
    form.send_keys(Keys.RETURN)
    time.sleep(10)
    table = driver.find_element_by_xpath('//*[contains(text(), "Host Records (A) ")]/following-sibling::div')
    rows = table.find_elements_by_tag_name('tr')

    for row in rows:
        subdomain = row.find_elements_by_tag_name('td')[0]
        subdomain = subdomain.text[:subdomain.text.find('\n')]
        subdomains.append(subdomain)
except Exception as e:
    print('Error while parsing dnsdumster')
    print(e)
try:
    driver.get(f'http://searchdns.netcraft.com/?host={domain}')
    time.sleep(10)
    table = driver.find_element_by_tag_name('tbody')
    rows = table.find_elements_by_tag_name('tr')
    for row in rows:
        subdomain = row.find_elements_by_tag_name('td')[1].text
        subdomains.append(subdomain)
except Exception as e:
    print('Error while parsing netcraft')
    print(e)

subdomains = set(subdomains)
subdomains = [{'subdomain': subdomain} for subdomain in subdomains]
basepath = os.path.dirname(__file__)
filepath = os.path.abspath(os.path.join(basepath, "..", "output", "domain_subdomains.json"))
with open(filepath, 'w') as f:
    json.dump(subdomains, f)

driver.quit()
