import time
import sys
import os
import json
from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options


domain = sys.argv[1]

options = Options()
options.add_argument('--headless')

driver = Firefox(options=options)
driver.get(f'http://toolbar.netcraft.com/site_report?url={domain}')
time.sleep(5)
history = driver.find_element_by_id('history_table')
table = history.find_element_by_tag_name('tbody')
rows = table.find_elements_by_tag_name('tr')
table_data = []
for row in rows:
    cells = row.find_elements_by_tag_name('td')
    values = [cell.text for cell in cells]
    table_data.append({
        'netblock_owner': values[0],
        'ip_address': values[1],
        'os': values[2],
        'web_server': values[3],
        'last_seen': values[4]
    })
driver.quit()
basepath = os.path.dirname(__file__)
filepath = os.path.abspath(os.path.join(basepath, "..", "output", "domain_history.json"))
with open(filepath, 'w') as f:
    json.dump(table_data, f)

