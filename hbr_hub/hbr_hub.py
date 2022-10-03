import urllib.request
from html.parser import HTMLParser
import re
import urllib.request
import os
from datetime import datetime
import webbrowser
import codecs

HBR_ARTICLES_LIST = 'hbr_articles_list.txt'
HBR_ARTICLES_PATH = 'articles'
HBR_ARTICLES_DEPTH = 100

def articles_list_download(url):
    target_titles_table = dict()
    source = ''
    class MyHTMLParser(HTMLParser):
        data_print_switcher = 0
        def handle_starttag(self, tag, attrs):
            if tag == 'a':
                # ('class', 'post__title_link')('href', 'https://habrahabr.ru/hub/programming/')
                if len(attrs) > 1 and 'post__title_link' in attrs[1]:
                    title_address = attrs[0][1]
                    title_name = 'current'
                    target_titles_table.update({title_name: title_address})
                    self.data_print_switcher = 1
        def handle_data(self, data):
            if self.data_print_switcher > 0:
                title_name = data
                title_address = target_titles_table.pop('current')
                target_titles_table.update({title_name : title_address})
                self.data_print_switcher = 0    
    for page_num in range(1, HBR_ARTICLES_DEPTH + 1):
        page_url = url + '/page' + str(page_num)
        print(page_url)
        source += urllib.request.urlopen(page_url).read().decode('utf-8')
        print(str(int(round(len(source) / 1024, 0))) + ' kB')
    parser = MyHTMLParser()
    parser.feed(source)
    filename = HBR_ARTICLES_LIST
    f = open(filename, 'w', encoding='utf8')
    for key, val in target_titles_table.items():
        f.write(key + '\n')
        f.write(val + '\n')
    f.close()

def filename_check(filename):
    for c in r'\/:*?"<>|':
        filename = filename.replace(c, ' ')
    filename = filename.replace('\n', ' ')
    filename = re.sub(' +', ' ', filename).strip()
    return filename


def article_download(url):
    source = urllib.request.urlopen(url).read().decode('utf-8')
    target_title_start_template = r'<title>'
    target_title_end_template = r'</title>'
    title = source[ source.find(target_title_start_template) +
        len(target_title_start_template) : \
        source.find(target_title_end_template) ]
    filename = os.path.join(HBR_ARTICLES_PATH, filename_check(title) + '.html')
    if os.path.isfile(filename):
        print('passed')
        return
    header = r'<!DOCTYPE html><html ><head>' + \
    '<meta http-equiv="content-type" content="text/html; charset=utf-8" />' + \
    '<title>' + title + '</title>' + '</head>'
    target_content_start_template = r'<div class="post__text post__text-html js-mediator-article">'
    target_content_end_template = r'<script id="js-mpf-mediator-init"'      
##    target_content_end_template = r'<dl class="defination-list defination-list_tags">'  
    content = source[ source.find(target_content_start_template) +
        len(target_content_start_template) : \
        source.find(target_content_end_template) ]

    target_images_table = dict()
    images_subpath = filename_check(title) + '_files'
    images_fullpath = os.path.join(HBR_ARTICLES_PATH, images_subpath)
    if not os.path.exists(images_fullpath):
        os.makedirs(images_fullpath)
##    print('{}, {}'.format(images_subpath, images_fullpath))
    class MyHTMLParser(HTMLParser):
        def handle_starttag(self, tag, attrs):
            if tag == 'img':
                for attr in attrs:
                    if attr[0] == 'src':
                        image_source_orig = attr[1]
                        image_source_name = image_source_orig.split(r'/')[-1]
                        image_source_new = '{}/{}'.format(images_subpath, image_source_name)
##                        print('{}, {}, {}'.format(image_source_name, image_source_orig, image_source_new))
                        try:
                            urllib.request.urlretrieve(image_source_orig, os.path.join(images_fullpath, image_source_name))                            
                        except:
                            pass
                        finally:
                            target_images_table.update({image_source_new : image_source_orig})
    parser = MyHTMLParser()
    parser.feed(content)
    for image_source_new, image_source_orig in target_images_table.items():
        content = content.replace(image_source_orig, image_source_new)
    f = open(filename, 'w', encoding='utf8')
    f.write(header)
    f.write('<body>' + '<h1>' + title + '</h1>' + content + '</body></html>')
    f.close()

def article_downloads():
    d = {}
    filename = HBR_ARTICLES_LIST
    if not os.path.exists(HBR_ARTICLES_PATH):
        os.makedirs(HBR_ARTICLES_PATH)    
    f = open(filename, 'r', encoding='utf8')
    l = f.read().splitlines()
    for i in range(0, len(l), 2):
        d.update({l[i] : l[i+1]})
    total = int(len(l)/2)
    counter = 0; 
    for key, val in d.items():
        print ('process page #{0}/{1} {2}'.format(counter, total, key))
        try:
            article_download(val)
        except:
            print('failed')
        finally:
            counter += 1
        
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

def build_articles_index(title = 'Python articles'):
    articles_votes = dict()
    for file in os.listdir(HBR_ARTICLES_PATH):
        if os.path.isfile(os.path.join(HBR_ARTICLES_PATH, file)) and file.endswith('.html'):
            with codecs.open(os.path.join(HBR_ARTICLES_PATH, file), 'r', 'utf-8') as f:
                content = f.read()
            try:
                vote = int(re.search('(title=\"Всего голосов )(.*?)(\:)', content)[2])
            except:
                vote = 0
            articles_votes[file] = vote
    articles_votes_sorted = dict(sorted(articles_votes.items(), key=lambda item: item[1], reverse = True))
    links = dict()
    for key, value in articles_votes_sorted.items():
        links[f'[{value}] {key.replace(" Хабр.html", "")}'] = os.path.join(HBR_ARTICLES_PATH, key)
    index = html_write(title, title, title, html_create(title, links))
    return index

## mode: 0 - rebuild & download, -1 - download list only, 1 - download pages only
def hbr_hub(hub_name = 'python', mode = 0):
    if mode <= 0:
        url = 'https://habrahabr.ru/hub/{}'.format(hub_name)
        print('LIST DOWNLOAD')
        articles_list_download(url)
    if mode >= 0:
        print('PAGES DOWNLOAD')
        article_downloads()
    print('INDEX BUILD')
    webbrowser.open(build_articles_index())
    print('FINISHED')


hbr_hub('python', 0)
