import requests
import csv
from lxml import html
from lxml import etree
import re
import glob
import codecs
import sys
import logging
import os

## Download items with magnet-links [very slow]
DEEPSCAN_MODE = False
## Use TOR: http(s): socks5://127.0.0.1:9150
USE_TOR = False

logging.basicConfig(
    level=logging.DEBUG, 
    format='%(asctime)s : %(levelname)s : %(message)s', 
    filename = 'rutracker_ratings.log', 
    filemode = 'w', 
)

def progress_print(iteration, total, prefix = '', suffix = '', decimals = 2, barLength = 40):
    filledLength    = int(round(barLength * iteration / float(total)))
    percents        = round(100.00 * (iteration / float(total)), decimals)
    bar             = '#' * filledLength + '-' * (barLength - filledLength)
    sys.stdout.write('%s [%s] %s%s %s\r\n' % (bar, percents, '%', suffix, prefix)),
    sys.stdout.flush()
    if iteration == total:
        print("\r\n")

def download(sections):
    counter = 0    
    dump_lxml = []
    section_total = len(sections)
    logging.info('sections {}'.format(section_total))
    logging.info('download started')    
    section_counter = 0
    for section_base_id in sections:
        section_counter += 1
        try:
            session = requests.session()
            if USE_TOR:
                session.proxies = {'http':  'socks5://127.0.0.1:9150',
                                   'https': 'socks5://127.0.0.1:9150'}
            site_base_url = 'https://rutracker.org'
            page_base_url = '{}/forum/viewforum.php?f={}'.format(site_base_url, section_base_id)
            r = session.get(page_base_url)
            section_info_lxml = html.fromstring(r.text).xpath('.//table[@class="w100"]')[0]
            page_offset_start = 0        
            page_offset_end = int(str(section_info_lxml.xpath('//a[@class="pg"]/@href')[-2]).split('=')[-1])
            page_offset_step = 50        
            page_title = str(section_info_lxml.xpath('//h1[@class="maintitle"]/a/text()')[0])
            logging.info('section {}'.format(page_title))
            progress_print(counter, section_total, prefix = '{}:'.format(page_title))
            with open('{}.csv'.format(filename_check(page_title)), 'w', newline='') as csvfile:
                csv.writer(csvfile, delimiter='\t').\
                                    writerow(["Score", "Title", "Description", "Direct Download Link"])        
                for page_offset in range(page_offset_start, page_offset_end, page_offset_step):
                    logging.info('process section {}:'.format(page_title))                    
                    try:
                        url = '{}&start={}'.format(page_base_url, page_offset)
                        r = session.get(url)
                        page_lxml = html.fromstring(r.text).xpath('//table[@class="vf-table vf-tor forumline forum"]')[0]
                    except:
                        logging.error('error: receive page elements {}'.format(url))
                        continue
                    for rec_lxml in page_lxml.xpath('//tr[@class="hl-tr"]'):
                        try:
                            title = str(rec_lxml.xpath('.//a[@class="torTopic bold tt-text"]/text()')[0])                
                            url = str(rec_lxml.xpath('.//a[@class="torTopic bold tt-text"]/@href')[0])
                            url = '{}/forum/{}'.format(site_base_url, url)
                            magnet = '-'
                            if DEEPSCAN_MODE:
                                try:
                                    
                                    r = session.get(url)
                                    magnet = str(html.fromstring(r.text).xpath('//a[@class="magnet-link"]/@href')[0])
                                except:
                                    logging.warning('warning: no magnet link at {}'.format(url))
                            try:
                                seeds = int(rec_lxml.xpath('.//span[@class="seedmed"]/b/text()')[0])
                            except:
                                seeds = -1
                                logging.warning('warning: no seeds at {}'.format(url))                        
                            csv.writer(csvfile, delimiter='\t').\
                                                writerow([seeds, title, url, magnet])
                        except:
                            logging.error('error: receive element {}'.format(url))
                            continue                        
                    pass
                pass
        except:
            logging.error('error: receive page info {}'.format(page_base_url))
        logging.info('download section complete')
        counter += 1
    progress_print(section_total, section_total, prefix = '')
    logging.info('downloaded {} items'.format(counter))    

def filename_check(filename):
    for c in r'\/:*?"<>|':
        filename = filename.replace(c, ' ')
    filename = filename.replace('\n', ' ')
    filename = re.sub(' +', ' ', filename).strip()
    return filename

def html_write(filename, title, content):
    filename = filename_check(filename) + '.html'
    header = r'<!DOCTYPE html>'+ '\n' + '<html>' + '\n' + '<head>' + '\n' + \
    '<meta http-equiv="content-type" content="text/html; charset=utf-8" />' + \
    '\n' + '<title>' + title + '</title>' + '\n' + '</head>' + '\n'
    author = str('By Author')
    f = open(filename, 'w', encoding='utf8')
    f.write(header + '<body>')
    f.write('<h1>' + title + '\n' + '</h1>' + content + '\n' + \
            '<hr/>\n' + author + '\n')
    f.write('</body>' + '\n' + '</html>')
    f.close()
    return filename

def export(score_min=1):
    counter = 0    
    output = []
    sources = glob.glob('*.csv')  
    logging.info('export started')
    for file_name in sources:
        progress_print(counter, len(sources), prefix = '{}:'.format(file_name))
        with open(file_name, 'r') as f:
            csv_reader = csv.reader(f, delimiter='\t')
            rows = list(row for row in csv_reader if row[0].isdigit())
        if len(rows) < 1:
            continue
        counter += 1
        rows = sorted((row for row in rows if int(row[0]) >= score_min), key=lambda x: int(x[0]), reverse=True)
        if DEEPSCAN_MODE:
            content = '<tr><th>Score</th><th>Title & Description link</th><th>Direct download link</th></tr>'
        else:
            content = '<tr><th>Score</th><th>Title & Description link</th></tr>'
        row_counter = 0
        for row in rows:
            if DEEPSCAN_MODE:
                content += '<tr><td>{}</td><td><a href={}>{}</a></td><td><a href={}>DOWNLOAD DIRECT</a></td></tr>'.format(row[0],row[2],row[1],row[3])
            else:
                content += '<tr><td>{}</td><td><a href={}>{}</a></td></tr>'.format(row[0],row[2],row[1])            
                
            row_counter += 1
        content = '<table>{}</table>'.format(content)
        html_write(os.path.splitext(file_name)[0], os.path.splitext(file_name)[0], content)
    progress_print(len(sources), len(sources))
    logging.info('exported {} items'.format(counter))
    return counter

def organize():
    counter = 0    
    lines = ''
    rules = dict()
    lines = load_sections_map().split('\r\n')
    curr_section = ''
    curr_value = ''
    for line in lines:
        if not '+++' in line:
            curr_section = line
            rules[curr_section] = ''
        else:
            curr_value = re.findall(r"(\+\+\+ )(.*?) \[([A-Za-z0-9_]+)\]", line)[0][1]
            rules[curr_section] = rules[curr_section] + curr_value + '; '
    sources = glob.glob('*.html')  
    logging.info('organize started')
    for file_name in sources:
        progress_print(counter, len(sources), prefix = '{}:'.format(file_name))        
        file_folder = ''
        try:
            file_folder = filename_check([key for key, value in rules.items() if os.path.splitext(file_name)[0] in value][0])
            counter += 1
        except:
            file_folder = 'Неразобранное'
        if not os.path.isdir(file_folder):
            os.mkdir(file_folder)
        if os.path.isfile(os.path.join(file_folder, file_name)):
            os.remove(os.path.join(file_folder, file_name))
        os.rename(file_name, os.path.join(file_folder, file_name))
    progress_print(len(sources), len(sources))
    logging.info('organized {} items'.format(counter))


def analize():
    subsections = {}
    logging.info('analize started')
    try:
        session = requests.session()
        if USE_TOR:
            session.proxies = {'http':  'socks5://127.0.0.1:9150',
                               'https': 'socks5://127.0.0.1:9150'}
        site_base_url = 'https://rutracker.org'
        map_base_url = '{}/forum/index.php?map'.format(site_base_url)
        r = session.get(map_base_url)
        map_info_lxml = html.fromstring(r.text).xpath('.//div[@id="f-map"]')[0]
        sections_lxml = map_info_lxml.xpath('//ul[@class="tree-root"]')
        with codecs.open('sections.txt', 'w', 'utf-8') as f:
            for section_lxml in sections_lxml:
                section_name = section_lxml.xpath('.//span[@class="c-title"]/@title')[0]
                subsections_refs = section_lxml.xpath('.//span/a/@href')
                subsections_names = section_lxml.xpath('.//span/a/text()')
                f.write('{}\r\n'.format(section_name))
                for subsection_name, subsection_ref in zip(subsections_names, subsections_refs):
                    subsections.update({subsection_name : subsection_ref})
                    f.write('+++ {} [{}]\r\n'.format(subsection_name, subsection_ref))
    except:
        logging.error('error: receive map info {}'.format(map_base_url))
    logging.info('analize complete')

def load_sections_map():
    try:
        with codecs.open('sections.txt', 'r', 'utf-8') as f:
            sections = f.read()
    except:
        print('Incorrect sections.txt: download sections map at first')
    return sections

def main():
    global DEEPSCAN_MODE
    print('1. Download (scan and download items)')    
    print('2. Export (sort, filter and organize downloaded items)')
    print('3. Analize (analize and download sections map of items)')    
    print('0. Enable deepscan (download items with magnet-links [very slow])')
    menu_id = None
    while (True):
        print('Enter operation: ')
        menu_id = input()
        if not menu_id.isdigit():
            continue
        else:
            menu_id = int(menu_id)
        if menu_id == 1:
            sections = ''
            print('enter section IDs in format "XXX,XXX,...,XXX" or press Enter for loading sections.txt: ')
            sections = input()
            if not sections:
                sections = re.findall(r"\[([A-Za-z0-9_]+)\]", load_sections_map())
                print('{} sections loaded'.format(len(sections)))
            else:
                sections = sections.split(',')                
            print('downloading...')
            download(sections)          
        elif menu_id == 2:
            print('enter filter level (min score value) or press Enter for set default value [1]: ')
            score_min = input()
            if not score_min:
                score_min = 1
            print('exporting and organizing...')
            print('exported:  {}'.format(export(int(score_min))))
            print('organized: {}'.format(organize()))
        elif menu_id == 3:
            print('analizing map...')
            analize()           
        elif menu_id == 0:
            print('switching deepscan mode to...')
            DEEPSCAN_MODE = not DEEPSCAN_MODE
            print(DEEPSCAN_MODE)
        else:
            continue
        print('Complete\n')

if __name__ == "__main__":
    main()
