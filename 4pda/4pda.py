from selenium.webdriver.firefox.options import Options
from selenium.webdriver.chrome.service import Service
from selenium import webdriver
from lxml import html
import pandas as pd
import webbrowser
import pickle
import codecs
import time
from multiprocessing import Pool
from multiprocessing.dummy import Pool as ThreadPool
from dataclasses import dataclass

codecs.register_error("strict", codecs.ignore_errors)

@dataclass
class Resource():
    name: str = ()
    records_counter: int = 0
    records_number_max: int = 100
    pages_number_max: int = 10
    records_score_min: int = 1
    comments_score_min: int = 1
    comments_convertion_min: int = 0
    hw_threads: int = 4
    def download_content(self, target_url, target_assert_text='Показать', target_assert_click='True'):
        options = Options()
        options.add_argument('--headless')
        service = Service(r'C:\Tools\GeckoDriver\geckodriver.exe')
        service.start()
        driver = webdriver.Remote(service.service_url, options=options)
        content = ''
        print(target_url)
        try:
            driver.get(target_url)
            element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.PARTIAL_LINK_TEXT , target_assert_text)))
            if target_assert_click:
                driver.find_element_by_partial_link_text(target_assert_text).click()
        except:
            pass
        while True:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(1)
            if content != driver.page_source:
                content = driver.page_source
                continue
            else:
                break
        driver.quit()
        return content

    def download_data(self):
        base_url = 'http://4pda.ru/'
        pages_total = self.pages_number_max
        page_ulrs = [f'{base_url}page/{page}/' for page in range(1, 1+pages_total)]
        records = dict()
        records_counter = 0
        for page_num in range(pages_total):
            print(f'proccessing page {page_num+1}/{pages_total}')
            page_content = self.download_content(page_ulrs[page_num], 'зарегистрированный товарный знак', False)
            page_tree = html.fromstring(page_content)
            page_records = page_tree.xpath('//article[@class="post"]')
            for i in range(len(page_records)):
                records_counter += 1
                if records_counter > self.records_number_max: break
                record_url = 'http:' + page_records[i].xpath('.//a[@rel="bookmark"]')[0].get('href')
                records[record_url] = ''
            if records_counter > self.records_number_max: break
        records_total = len(records)
        pool = ThreadPool(self.hw_threads)
        records_urls = records.keys()
        records_content = pool.map(self.download_content, records_urls)
        pool.close()
        pool.join()
        records = dict(zip(records_urls, records_content))
        with codecs.open(f'{self.name}.dump', 'wb') as f:
            pickle.dump(records, f)

    def analize_content_ref(self, content, pattern, index = -1, default = ''):
        result = default
        try:
            if index < 0:
                result = html.fromstring(content).xpath(pattern).get('href')
            else:
                result = html.fromstring(content).xpath(pattern)[index].get('href')
        except:
            # print(f'ERR: {pattern}\n{content}')
            pass
        return result

    def analize_content(self, content, pattern, index = -1, default = ''):
        result = default
        try:
            if index < 0:
                result = html.fromstring(content).xpath(pattern)
            else:
                result = html.fromstring(content).xpath(pattern)[index]
        except:
            # print(f'ERR: {pattern}\n{content}')
            pass
        return result

    def analize_data(self):
        with codecs.open(f'{self.name}.dump', 'rb') as f:
            records = pickle.load(f)
        content = ''
        for record_url, record_content in records.items():
            r = record_content
            link = record_url
            title = self.analize_content(r, './/h1[@itemprop="name"]//text()', 0).strip()
            text = ''.join(self.analize_content(r, './/div[@itemprop="articleBody"]//text()')).replace('\n', ' ').strip()
            date = self.analize_content(r, './/em[@class="date"]//text()', 0).strip()
            author = self.analize_content(r, './/span[@class="name"]//text()', 0).strip()
            score = self.analize_content(r, './/a[@class="number"]//text()', 0).strip()
            comments = self.analize_content(r, './/div[contains(@id, "comment")]')
            comments_total = len(comments)
            df = pd.DataFrame(columns=['Оценка', 'Текст', 'Автор', 'Дата', 'Ссылка'], index=range(len(comments)))
            for i in range(comments_total):
                c = html.tostring(comments[i])
                df.loc[i, 'Оценка'] = self.analize_content(c, './/span[@class="num"]//text()', 0).strip()
                df.loc[i, 'Текст'] = ' '.join(self.analize_content(c, './/p[@class="content"]//text()')).replace('\n', '').strip()
                df.loc[i, 'Автор'] = self.analize_content(c, './/a[@class="nickname"]//text()', 0).strip()
                df.loc[i, 'Дата'] = self.analize_content(c, './/span[@class="h-meta"]//text()', 0).replace('|', '').strip()
                df.loc[i, 'Ссылка'] = link + self.analize_content_ref(c, './/span[@class="more-meta"]//a', 0).strip()
                i += 1
            df['Дата'] = pd.to_datetime(df['Дата'])
            df['Оценка'] = pd.to_numeric(df['Оценка'])
            df = df.loc[df['Оценка'] >= 1]
            comments_positive = len(df.index)
            comments_convertion = int(100*comments_positive/comments_total)
            df = df.loc[df['Оценка'] >= self.comments_score_min]
            df = df.drop_duplicates(subset='Ссылка', keep='last')
            df = df.sort_values(by=['Оценка'], ascending=False)
            if score.isnumeric() and int(score) >= self.records_score_min and comments_convertion >= self.comments_convertion_min:
                content += f'<b>{title}</b><br><br> \
                    Высказались по теме {comments_total} чел., \
                    из них было положительных {comments_positive} ответов ({comments_convertion})%, наиболее оцененные ответы:<br><br> \
                    {df.to_html(index=False)}<br><br> \
                    {text}<br><br>{date} by {author} (+{score})<br>{link}<hr/><br>'
        with codecs.open(f'{self.name}.html', 'w', 'utf-8') as f:
            f.write(content)
        webbrowser.open(f'{self.name}.html')

    def run(self, mode=1):
        if mode == 0: # mode 0: download & analize
            self.download_data()
        if mode >= 0: # mode 1: analize only
            self.analize_data()

res = Resource(name='4pda', records_number_max=50, pages_number_max=3, records_score_min=25, comments_score_min=5, comments_convertion_min=30, hw_threads=8)
res.run(mode=0)
