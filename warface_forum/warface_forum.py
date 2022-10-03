from netstream import Netstream
import codecs
import pickle
import lxml
import pandas as pd
import sys

## network mode: -1 - No Proxy, 0 - TOR Proxy, 1 - Random Proxy
mode = 0
## maximum network connections: 1 .. 100 (recommended: 10)
connections_max = 10
## download and update data into dumps (*.pickle)
download_updates_threads_info = True
download_updates_threads_content = True

def progress_bar (iteration, total, prefix = '', suffix = '', decimals = 2, bar_length = 100):
    filled_length = int(round(bar_length * iteration / float(total)))
    percents = round(100.00 * (iteration / float(total)), decimals)
    bar = '#' * filled_length + '-' * (bar_length - filled_length)
    sys.stdout.write(f'{prefix} [{bar}] {percents}{"%"} {suffix}\r'), sys.stdout.flush()
    if iteration == total: print('\n')

def get_threads_info(thread, download_updates=True):
    thread_id = thread[0]
    thread_title = thread[1]
    pages_max = 1
    urls = [f'https://ru.warface.com/forums/forumdisplay.php?f={thread_id}&page={page_num}&order=desc/' for page_num in range(1,1+pages_max)]
    if download_updates:
        netstream = Netstream()
        received, total, content = netstream.download(mode=mode, targets=urls)
        if received == total:
            with codecs.open(f'{thread_id}.pickle', 'wb') as f:
                pickle.dump(content, f)
    df = pd.DataFrame(columns = ['score', 'text', 'date', 'link'])
    pages = dict()
    with codecs.open(f'{thread_id}.pickle', 'rb') as f:
        pages = pickle.load(f)
    for page in pages.values():
        records = lxml.html.fromstring(page).xpath('.//li[contains(@id, "thread_")]')
        for record in records:
            date = record.xpath('.//em[@class="time"]//text()')[0]
            link = record.xpath('.//a[@class="title"]')[0].get('href')
            text = record.xpath('.//a[@class="title"]//text()')[0]
            score = record.xpath('.//div[@class="thread_like"]//div//text()')[0]
            row = pd.DataFrame([[score, text, date, link]], columns = ['score', 'text', 'date', 'link'])
            df = df.append(row)
    df = df.drop_duplicates(subset=df.columns.difference(['link']))
    df['score'] = pd.to_numeric(df['score'])
    df = df.sort_values(by=['score'], ascending=False)
    df = df[df['score'] > 0]
    df['link'] = df['link'].apply(lambda x: '<a href="https://ru.warface.com/forums/{0}">view</a>'.format(x))
    content = f'<h3><a href="{urls[0]}">{thread_title}</a></h3>'
    content += df.to_html(index=False, escape=False).replace(r'\n', '<br>')
    with codecs.open(f'{thread_id}.html', 'w') as f:
        f.write(content)
    threads_ids = [item[56:62] for item in df['link'].tolist()]
    threads_titles = [item for item in df['text'].tolist()]
    return dict(zip(threads_ids, threads_titles))

def get_thread_messages(thread, download_updates=True):
    thread_id = thread[0]
    thread_title = thread[1]
    pages_max = 1
    first_page_url = f'https://ru.warface.com/forums/showthread.php?t={thread_id}'
    if download_updates:
        print(f'downloading thread {thread_id}: {thread_title}...')
        pages = dict()
        netstream = Netstream()
        try:
            received, total, content = netstream.download(mode=mode, targets=[first_page_url])
            pages_control = lxml.html.fromstring(content[first_page_url]).xpath('.//a[@class="popupctrl"]//text()')[3]
            pages_max = int(pages_control[pages_control.index('из ')+3:])
            print(f'total pages in thread: {pages_max}')
        except:
            print('download error: index passed')
        urls = [f'https://ru.warface.com/forums/showthread.php?t={thread_id}&page={page_num}/' for page_num in range(1,1+pages_max)]
        netstream = Netstream()
        urls_groups = list(zip(*[iter(urls)] * connections_max))
        for url_group in urls_groups:
            try:
                received, total, content = netstream.download(mode=mode, targets=url_group)
                pages.update(content)
            except:
                print('download error: group passed')
            progress_bar(len(pages), pages_max, prefix = 'progress:', suffix = 'Complete', bar_length = 50)
        with codecs.open(f'{thread_id}.pickle', 'wb') as f:
            pickle.dump(pages, f)
        print('pages download complete')
    else:
        print('download passed')
    print(f'parsing thread {thread_id}...')
    df = pd.DataFrame(columns = ['score', 'text', 'date', 'link'])
    pages = dict()
    with codecs.open(f'{thread_id}.pickle', 'rb') as f:
        pages = pickle.load(f)
    for url in pages.keys():
        try:
            records = lxml.html.fromstring(pages[url]).xpath('.//li[@class="postbitlegacy postbitim postcontainer"]')
        except:
            print(f'error parsing page {url}')
            continue
        for record in records:
            try:
                date = record.xpath('.//span[@class="postdate old"]//text()')[1] + record.xpath('.//span[@class="postdate old"]//text()')[2]
                link = record.xpath('.//a[@class="postcounter"]')[0].get('href')
                text = ''.join([f'{p.strip()}\n' for p in record.xpath('.//div[@class="content"]//text()')])
                score = record.xpath('.//div[@class="post_like"]//div//text()')[0]
                row = pd.DataFrame([[score, text, date, link]], columns = ['score', 'text', 'date', 'link'])
                df = df.append(row)
            except:
                print(f'error parsing record {record}')
                continue
    df = df.drop_duplicates()
    df['score'] = pd.to_numeric(df['score'])
    df = df.sort_values(by=['score'], ascending=False)
    df = df[df['score'] > 0]
    df['link'] = df['link'].apply(lambda x: '<a href="https://ru.warface.com/forums/{0}">view</a>'.format(x))
    content = f'<h3><a href="{first_page_url}">{thread_title}</a></h3>'
    content += df.to_html(index=False, escape=False).replace(r'\n', '<br>')
    with codecs.open(f'{thread_id}.html', 'w', 'utf-8') as f:
        f.write(content)

threads_info = dict(zip(['22', '82'], ['Обсуждение игры', 'Оружейная комната']))
for thread_info in threads_info.items():
    print(f'reading root thread {thread_info}...')
    threads = get_threads_info(thread_info, download_updates=download_updates_threads_info)
    print(f'threads to process: {threads}')
    for thread in threads.items():
        get_thread_messages(thread, download_updates=download_updates_threads_content)
