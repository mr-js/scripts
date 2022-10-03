import feedparser
from datetime import datetime, timedelta
from time import mktime
import configparser
import webbrowser
import re


def filename_check(filename):
    for c in r'\/:*?"<>|':
        filename = filename.replace(c, ' ')
    filename = filename.replace('\n', ' ')
    filename = re.sub(' +', ' ', filename).strip()
    return filename


def html_write(filename, title, subtitle, content):
    filename = filename_check(filename) + '.html'  
    header = r'<!DOCTYPE html>'+ '\n' + '<html>' + '\n' + '<head>' + '\n' + \
    '<meta http-equiv="content-type" content="text/html; charset=utf-8" />' + \
    '\n' + '<title>' + title + '</title>' + '\n' + '</head>' + '\n' + \
    '<style>a {text-decoration: none;} </style>' + '\n'
    f = open(filename, 'w', encoding='utf8')
    f.write(header + '<body style="font-family:Arial">' + '\n')
    f.write(content + '\n' + subtitle + '\n')
    f.write('</body>' + '\n' + '</html>')
    f.close()
    return filename


def html_create(name, links):
    links_list = links.items()
    html_list = ''
    if (len(links_list) == 0):
        html_list = 'None'
    else:
        for key, value in links_list:
            html_list += '<li><a target="_blank" href="{0}">{1}</a></li>\n'.format(value, key) 
    html_list = '<h3>{}</h3>\n<hr/>\n<ul>\n{}</ul>\n<hr/>\n'.format(name, html_list)
    return html_list


def rss_feed(url, name, new=None, keywords=None, limit=100):
    links = {}
    rss = feedparser.parse(url)
    counter = 0
    for entry in rss.entries:
        try:
            date = datetime.fromtimestamp(mktime(entry.published_parsed))
        except:
            date = datetime.today()
        if new == None or datetime.today() - date < timedelta(days=new):
            if keywords == None or any(str.strip(keyword).lower() in entry.title.lower() for keyword in keywords if keyword != ''):
                links[entry.title] = entry.link
                counter += 1
                if counter >= limit:
                    break
    return html_create(name, links)


def rss_feeds():
    print('started')
    content = ''
    config = configparser.RawConfigParser()
    config.optionxform = str
    config.read('rss_master.ini', encoding='utf-8')
    if config.getboolean('COMMON', 'UseKeywordsFilter'):
        keywords = str.split(str(config.get('COMMON', 'Keywords')), ',')
##        print('keywords: {}'.format(', '.join(map(str, keywords))))
    else:
        keywords = None
    age = int(config.get('COMMON', 'NewsDaysOld'))
    limit = int(config.get('COMMON', 'NewsRecordsLimit'))
    title = str(config.get('COMMON', 'Title'))
    filename = str(config.get('COMMON', 'FileName'))     
    for key in config['FEED LIST']:
        print('source: {}'.format(key))
        content += rss_feed(config.get('FEED LIST', key), key, age, keywords, limit)
    timestamp = str(datetime.today().strftime('%d.%m.%Y %H:%M:%S'))
    signature = 'Generated at {} by RSS Master'.format(timestamp)
    result = html_write(filename, title, signature, content)
    if config.getboolean('COMMON', 'AutoOpen'):
        webbrowser.open(result)
    print('finished')


rss_feeds()
