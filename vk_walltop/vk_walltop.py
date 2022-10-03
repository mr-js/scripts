import pickle
import urllib.request
import json
from datetime import datetime
import os
import sys
import webbrowser
import re


non_bmp_map = dict.fromkeys(range(0x10000, sys.maxunicode + 1), '')


def printProgress (iteration, total, prefix = '', suffix = '', decimals = 2, barLength = 100):
    filledLength    = int(round(barLength * iteration / float(total)))
    percents        = round(100.00 * (iteration / float(total)), decimals)
    bar             = '#' * filledLength + '-' * (barLength - filledLength)
    sys.stdout.write('%s [%s] %s%s %s\r' % (prefix, bar, percents, '%', suffix)),
    sys.stdout.flush()
    if iteration == total:
        print("\n")


def filename_check(filename):
    for c in r'\/:*?"<>|':
        filename = filename.replace(c, ' ')
    filename = filename.replace('\n', ' ')
    filename = re.sub(' +', ' ', filename).strip()
    return filename


def download_image(url, wallName):
    target_images_subpath = filename_check(wallName) + '_files'
    target_images_fullpath = os.path.join('output', filename_check(target_images_subpath))
    if not os.path.exists(target_images_fullpath):
        os.makedirs(target_images_fullpath)
    orig_img_src = url
    img_name = orig_img_src.split(r'/')[-1]
##    new_img_src = os.path.join(target_images_subpath, img_name)
    try:
        urllib.request.urlretrieve(orig_img_src, os.path.join(target_images_fullpath, img_name))
    finally:
        return os.path.join(target_images_subpath, img_name)

    
def print_wall_info(id, name, top, depth):
    
    print('Analize {0} {1} for top-{2} with depth {3} records\n'.format(
        id,
        name,
        top,
        depth
        ))

    
def print_record_info(wall, record, position):
    
    title = str(record[1].split('\n')[0]).translate(non_bmp_map)
    print('-'*75)
    print('RECORD {0} (TOP-{1})'.format(record[0], position))
    print('-'*75)
    print('  {0}'.format(title))
    print('https://vk.com/wall-{0}_{1}'.format(wall, record[0]))
    print('+ {0} likes'.format(record[2]))


def format_record_info(wall, record, position):
    
    title = '{0}'.format(record[1].split('\n')[0]).translate(non_bmp_map)
    if len(title) == 0:
        title = 'Запись без заголовка'
    elif len(title) > 75:
        title = title[:72] + '.'*3
    content = '<hr/>\n' + \
        '<h5>ЗАПИСЬ TOP-{1}</h5>'.format(record[0], position) + '\n' + \
        '<p><a href="https://vk.com/wall-{0}_{1}'.format(wall, record[0]) + \
        '">' + title + '</a></p>' + '\n' + \
        '<p>+ {0} likes'.format(record[2]) + '</p>\n'
    return content


def format_record_content(wallID, wallName, record, position):
    
    title = '{0}'.format(record[1].split('\n')[0]).translate(non_bmp_map)
    text = '{0}'.format(record[1]).translate(non_bmp_map)
    if len(title) == 0:
        title = 'Запись без заголовка'
    if len(title) > 60:
        title = title[:60] + '.'*3
    if record[3] != '':
        #print(record[3])
        for attach in record[3]:
            if 'photo' in attach:
                #print('PHOTO DETECTED')
                sizes = []
                for item in attach['photo']:
                    if 'photo_' in item:
                        sizes.append(int(item.split('_')[1]))
                sizes.sort()
                image = download_image(attach['photo']['photo_' + str(sizes[-1])], wallName)
                #print(attach['photo']['photo_' + str(sizes[-1])])
                text += '\n' + '<p><img src="{0}" alt="{1}" style="width:100%;"></p>'.format(image, title) + '\n'

    text = '<div id="toggleText{0}" style="display: none;">'.format(position) + \
    '\n' + '<p>' + text.replace('\n', '</br>') + '</p>' + '\n' + \
    '</div>' + '\n'
    content = '<hr/>\n' + \
        '<h4>ЗАПИСЬ TOP-{1}</h4>'.format(record[0], position) + '\n' + \
        '<p><a href="https://vk.com/wall-{0}_{1}'.format(wallID, record[0]) + \
        '">' + title + '</a>' + \
        '<a href="javascript:toggle(\'toggleText{0}\', \'displayText{0}\');" id="displayText{0}">&nbsp;↓&nbsp;</a>'.format(position) + \
        text + \
        '<p>+ {0} likes'.format(record[2]) + '</p>\n'
    content = content + '\n'
    return content
    

def write_wall_top(title, content):

    filename = os.path.join('output', filename_check(title) + '.html')
    header = r'<!DOCTYPE html>'+ '\n' + '<html>' + '\n' + '<head>' + '\n' + \
    '<meta http-equiv="content-type" content="text/html; charset=utf-8" />' + \
    '\n' + '<title>' + title + '</title>' + '\n' + '</head>' + '\n'
    script = '<script>' + \
        'function toggle(toggleText, displayText)' + \
        '	{' + \
        '	var elmt = document.getElementById(toggleText);' + \
        '	var text = document.getElementById(displayText);' + \
        '	if(elmt.style.display == "block")' + \
        '	{' + \
        '		elmt.style.display = "none";' + \
        '		text.innerHTML = "&nbsp;&darr;&nbsp;";' + \
        '	}' + \
        '	else' + \
        '	{' + \
        '		elmt.style.display = "block";' + \
        '		text.innerHTML = "&nbsp;&uarr;&nbsp;";' + \
        '	}' + \
        '}' + \
        '</script>'
    timestamp = str(datetime.today())
    f = open(filename, 'w', encoding='utf8')
    f.write(header + '<body>')
    f.write('<h3>Журнал ' + title + '\n' + '</h3>' + content + '\n' + \
            '<hr/>\n' + timestamp + '\n')
    f.write('</body>' + '\n' + script + '\n' + '</html>')
    f.close()
    return filename
    

def create_wall_top(wallID, wallTop = 100, wallDepth = 0, mode = 0, wallName = ''):
    with open('access_key.txt', 'r') as f:
        wallAccessKey = f.read()
    if mode == 0 or mode == 1:
        req = 'https://api.vk.com/method/wall.get?&access_token={0}&owner_id=-{1}&extended=1&v=5.53'.format(wallAccessKey, wallID)
        opener = urllib.request.FancyURLopener({})
        with opener.open(req) as f:
            string  = f.read().decode('utf-8')
            json_obj = json.loads(string)
            if wallDepth == 0:
                wallDepth = int(json_obj['response']['count'])
            if wallName == '':
                wallName = str(json_obj['response']['groups'][0]['name'])
        print_wall_info(wallID, wallName, wallTop, wallDepth)
        records = []
        recordsCounter = 0
        printProgress(recordsCounter, wallDepth, prefix = 'Scan:', suffix = 'Complete', barLength = 50)
        for wallOffset in range(0, wallDepth, 100):
            req = 'https://api.vk.com/method/wall.get?&access_token={0}&owner_id=-{1}&offset={2}&count=100&v=5.53'.format(wallAccessKey, wallID, wallOffset)
            opener = urllib.request.FancyURLopener({})
            with opener.open(req) as f:
                string  = f.read().decode('utf-8')
                json_obj = json.loads(string)
                for item in json_obj['response']['items']:
                    if 'attachments' in item:
                        records.append([item['id'], item['text'], item['likes']['count'], item['attachments']])
                    else:
                        records.append([item['id'], item['text'], item['likes']['count'], ''])
                    recordsCounter += 1
                    if recordsCounter >= wallDepth:
                        break
            printProgress(recordsCounter, wallDepth, prefix = 'Scan:', suffix = 'Complete', barLength = 50)
        records = sorted(records, key=lambda record:record[2], reverse = True)
        pickle.dump(records, open(os.path.join('output', filename_check(wallName) + '.bin'), 'wb'))
    if mode == 1:
        return
    if mode == 0 or mode == 2:
        records = pickle.load(open(os.path.join('output', filename_check(wallName) + '.bin'), 'rb'))
        recordsCounter = 0
        output = ''
        for record in records:
            recordsCounter += 1
            if recordsCounter > wallTop:
                break
            else:
                #print_record_info(wallID, record, recordsCounter)
                output += format_record_content(wallID, wallName, record, recordsCounter)
                #output += format_record_info(wallID, record, recordsCounter)
                printProgress(recordsCounter, wallTop, prefix = 'Format:', suffix = 'Complete', barLength = 50)
        filename = write_wall_top(wallName, output)
        return filename


def input_param(name, default, datatype = 'str', description = ''):
    if description:
        print('/* {0} */'.format(description))
    print('Enter {0} (default value {1}): '.format(name, default))
    value = input()
    if datatype == 'str':
        return str(value or default)
    elif datatype == 'int':
        return int(value or default)


mode = input_param('mode', 0, 'int', 'Mode (0 - scan and format, 1 - scan only, 2 - format only)')
print('Switched to mode {0}\n'.format(mode))
wallID = input_param('wallID', 0, 'str', 'ID of target wall for scanning (0 - scan all walls from target_id.txt)')
if mode == 0:
    wallName = ''
    wallTop = input_param('wallTop', 100, 'int', 'TOP-level for target records (for example, 10 for get TOP-10)')
    wallDepth = input_param('wallDepth', 0, 'int', 'Depth of wall scanning in pages (0 - scan all wall pages)')
elif mode == 1:
    wallName = ''
    wallTop = 0
    wallDepth = input_param('wallDepth', 0, 'int', 'Depth of wall scanning in pages (0 - scan all wall pages)')
elif mode == 2:
    wallName = input_param('wallName', 'Шедевры рекламы', 'str', 'Name of a wall (the file <wallName>.bin)')
    wallTop = input_param('wallTop', 100, 'int', 'TOP-level for target records (for example, 10 for get TOP-10)')
    wallDepth = 0

if wallID != '0':
    result = str(create_wall_top(wallID, wallTop, wallDepth, mode, wallName))
    print('Done: {}'.format(result))
    if mode == 0 or mode == 2:
        webbrowser.open(result)
else:
    with open('target_id.txt', 'r') as f:      
        wallID_list = list(filter(lambda x: '#' not in x, f.read().split('\n')))
    for wallID in wallID_list:
        print('Done: {}'.format(str(create_wall_top(wallID, wallTop, wallDepth, mode, wallName))))
        pass
