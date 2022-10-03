from urllib.request import urlopen, Request
import requests
from urllib.parse import quote
import lxml
from lxml import html
from lxml.html.clean import Cleaner
from datetime import datetime
import json
import quopri
import codecs
import sys
import re
import os
import random
import time
from fake_useragent import UserAgent
import webbrowser
import configparser


non_bmp_map = dict.fromkeys(range(0x10000, sys.maxunicode + 1), 0xfffd)
## ! .* - NO,  .*? - YES !
cleaner = Cleaner(
    scripts=False, javascript=False, comments=False, style=False, links=True,
    meta=False, page_structure=False, processing_instructions=False,
    embedded=False, frames=False, forms=False, annoying_tags=False,
    remove_tags=[], allow_tags=[], remove_unknown_tags=False,
    safe_attrs_only=True, add_nofollow=True, host_whitelist=[],
    whitelist_tags = [])
gen_data = lambda x: ''.join(random.choice('QWERTYUIOPASDFGHJKLZXCVBNM1234567890') for i in range(x))    


class RECORD:
    ID = ''
    title = ''
    price = ''
    date = ''
    location = ''
    url = ''
    text = ''
    def __init__(self):
        self.ID = gen_data(16)
    def fill(self, title, price, date, location, url, text=''):
        self.title = title
        self.price = price
        self.date = date        
        self.location = location
        self.url = url  
        self.text = text
    def format(self):
        return '{}{}{}{}{}{}'.format(self.title, self.price, self.date, self.location, self.url, self.text) + '*'*80


def scan(request, region, user, depth=10, proxies=False, delay=0, details=False):
    ## records
    records = []
    page_counter = 1
    page_total = depth
    ## pages
    for page_counter in range(page_total):
        print('process page #{}'.format(page_counter+1))
        page_url = 'https://m.avito.ru/{}?user={}&p={}&bt=1&q='.format(region, user, page_counter)
        with requests.session() as s:
            ## antiban tor proxies
            if proxies == True:
                s.proxies = {'http':  'socks5://127.0.0.1:9150',
                               'https': 'socks5://127.0.0.1:9150'}
            ## antiban random user agents
            s.headers = {'User-Agent': UserAgent().chrome}
            try:
                r = s.get(page_url+quote(request))
            except requests.exceptions.RequestException:
                print('Connection error. Check TOR service status {}'.format(s.proxies))
                return None
            except Exception as e:
                print('ERROR: {}'.format(e))
                return None
            if details == True:
                print('User agent: {}\nIP: {}\n'.format(r.request.headers, json.loads(s.get('http://jsonip.com').text)["ip"]))
        items = html.fromstring(r.text).xpath('.//article')
        record_counter = len(items)
        if record_counter != 0:
            print('found {} records\n'.format(record_counter))
        else:
            err = cleaner.clean_html(r.text)
            if 'Доступ с вашего IP-адреса временно ограничен' or 'Доступ временно заблокирован' in err:
                print('IP BANNED')
                return
            else:
                print('Proccess error. See err.log for details')
                with open('err.log', 'w') as f:
                    f.write(err)
        ## records    
        for item in items:
            try:
                title = ''; price = ''; date = ''; location = ''; url = ''; text = ''
                url = item.xpath('.//a')[0].get('href')
                title = cleaner.clean_html(item.xpath('.//span[@class="header-text"]/text()')[0])
                date = cleaner.clean_html(item.xpath('.//div[@class="info-date info-text"]/text()')[0])
                price = cleaner.clean_html(item.xpath('.//span[@class="item-price-value"]/text()')[0])
                location = cleaner.clean_html(item.xpath('.//span[@class="info-text info-metro-district"]/text()')[0])
            except:
                pass
            record = RECORD()
            record.fill(title, price, date, location, url, text)
            records.append(record)
            record_counter += 1
        ## antiban delay (for more then 10 pages at once)
        if page_total > 1:
            time.sleep(delay)
    content = ''
    for record in records:
        content += '<tr><td>{}</td><td>{}</td><td>{}</td><td>{}</td><td>{}</td><td>{}</td></tr>'.format(
            record.title,
            record.price,
            record.date,
            record.location,
            '<a target="_blank" href="{}{}">{}</a>'.format('https://m.avito.ru/', record.url, record.url),
            record.text
            )
    content = '<table cellspacing="0" border="1" cellpadding="5" ><caption></caption>{0}</table>'.format(content)
    html_write('avito_watcher', content, 'output.html')
    webbrowser.open('output.html')
    return records


def html_write(title, content, filename):
    header = r'<!DOCTYPE html>'+ '\n' + '<html>' + '\n' + '<head>' + '\n' + \
    '<meta http-equiv="content-type" content="text/html; charset=utf-8" />' + \
    '\n' + '<title>' + title + '</title>' + '\n' + '</head>' + '\n'
    timestamp = str(datetime.today())
    f = open(filename, 'w', encoding='utf8')
    f.write(header + '<body>')
    f.write('<h1>' + title + '</h1>' + '\n' + content + '\n' + \
            '<hr/>\n' + timestamp + '\n')
    f.write('</body>' + '\n' + '</html>')
    f.close()
    return filename


config = configparser.RawConfigParser()
config.read('avito_watcher.ini')
if config.getboolean('COMMON', 'Active'):
    request = str(config.get('COMMON', 'Request'))
    region = str(config.get('COMMON', 'Region'))
    user = str(config.get('COMMON', 'User'))
    depth = int(config.get('COMMON', 'Depth'))
    proxies = config.getboolean('COMMON', 'Proxies')
    delay = int(config.get('COMMON', 'Delay'))
    details = config.getboolean('COMMON', 'Details')
    scan(request, region, user, depth, proxies, delay, details)
    print('Finished. Press any key to exit...')
    input()
else:
    print('Inactive settings in INI-file')
