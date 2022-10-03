from selenium import webdriver
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from lxml import html
import pandas as pd
import webbrowser
import pickle
import codecs
import time
from datetime import datetime
from dataclasses import dataclass
from contextlib import suppress
import nltk
import pymystem3
from dostoevsky.tokenization import RegexTokenizer
from dostoevsky.models import FastTextSocialNetworkModel
import re

codecs.register_error("strict", codecs.ignore_errors)
# ! RUN THIS AT FIRST TIME AT ONES !
# nltk.download()
# nltk.download('stopwords')


@dataclass
class RecordPattern():
    control: str = ()
    record: str = ()
    url: str = ()
    date: str = ()
    title: str = ()
    text: str = ()
    score: str = ()

@dataclass
class Resource():
    title: str = ()
    name: str = ()
    url: str = ()
    patterns: RecordPattern = None
    delay: int = 1
    records_counter: int = 0
    pages_number_max: int = 1
    comments_number_max: int = 1000
    valuable_comments_score: int = 10
    invaluable_comments_score: int = -2
    freq_number_max: int = 100

    def download_content(self, target_url):
        options = webdriver.FirefoxOptions()
        options.add_argument('--headless')
        driver = webdriver.Firefox(executable_path=GeckoDriverManager().install(), options=options)
        driver.get(target_url)
        element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.PARTIAL_LINK_TEXT , self.patterns.control)))
        scroll_counter = 1
        records_counter = 0
        content = ' '
        while True:
            scroll_counter += 1
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(self.delay)
            if records_counter > self.comments_number_max:
                print(f'breaking: maximum comments limit {self.comments_number_max} at scrolling collected')
                break
            if content != driver.page_source:
                content = driver.page_source
                try:
                    records_counter = len(html.fromstring(content).xpath(self.patterns.record))
                    print(f'page scrolled -- records reconized: {records_counter}')
                except:
                    pass
                continue
            else:
                break
        driver.quit()
        return content

    def download_data(self):
        pages_total = self.pages_number_max
        page_ulrs = [self.url]
        records_counter = 0
        df = pd.DataFrame(columns=['Оценка', 'Текст', 'Заголовок', 'Дата'])
        for page_num in range(pages_total):
            print(f'proccessing page {page_num+1}/{pages_total}: {page_ulrs[page_num]}')
            page_content = self.download_content(page_ulrs[page_num])
            page_tree = html.fromstring(page_content)
            page_records = page_tree.xpath(self.patterns.record)
            for i in range(len(page_records)):
                records_counter += 1
                if records_counter > self.comments_number_max:
                    print(f'breaking: maximum comments limit {self.comments_number_max} at parsing collected')
                    break
                url = ''; date = ''; title = ''; text = ''; score = ''
                with suppress(Exception):
                    url = page_records[i].xpath(self.patterns.url)[0].get('href')
                    date = page_records[i].xpath(self.patterns.date)[0]
                    title = page_records[i].xpath(self.patterns.title)[1]
                    text = page_records[i].xpath(self.patterns.text)[0]
                    score = page_records[i].xpath(self.patterns.score)[1]
                    df.loc[i, 'Дата'] = f'<a target="_blank" href="{url}">{date}</a>'
                    df.loc[i, 'Заголовок'] = title
                    df.loc[i, 'Текст'] = text
                    df.loc[i, 'Оценка'] = score
            if records_counter > self.comments_number_max: break
        records_total = len(df)
        print(f'total records: {records_total}')
        df['Оценка'] = pd.to_numeric(df['Оценка'])
        with codecs.open(f'{self.name}.dump', 'wb') as f:
            pickle.dump(df, f)

    def analize_emotion(self, model, text):
        messages = text.splitlines()
        results = model.predict(messages, k=2)
        scores_positive = 0.0; scores_negative = 0.0; scores_neutral = 0.0
        for message, sentiment in zip(messages, results):
            scores_positive += sentiment.get('positive', 0)
            scores_negative += sentiment.get('negative', 0)
            scores_neutral += sentiment.get('neutral', 0)
        return (int(100 * scores_negative), int(100 * scores_positive))

    def analize_data(self):
        df = pd.DataFrame(columns=['Оценка', 'Текст', 'Заголовок', 'Дата'])
        with codecs.open(f'{self.name}.dump', 'rb') as f:
            df = pickle.load(f)
        df = df.drop_duplicates(subset='Дата', keep='last')
        all_text = re.sub(r'([\n ])\1*', r'\1', df.to_string(columns=['Текст'], index=False).strip())
        sentiment_conversion = (0, 0, 0)
        all_text = '. '.join(p.strip() for p in all_text.splitlines())
        with codecs.open(f'{self.name}.txt', 'w', 'utf-8') as f:
            f.write(all_text)
        russian_stopwords = nltk.corpus.stopwords.words('russian')
        mystem = pymystem3.Mystem()
        tokens = mystem.lemmatize(all_text.lower())
        freq = nltk.FreqDist(token.lower() for token in tokens if token.isalpha() and token not in russian_stopwords).most_common(self.freq_number_max)
        frequency_analysis = pd.DataFrame(list(freq), columns = ['Любимое слово', 'Количество употреблений']).head(self.freq_number_max)
        comments_total = len(df)
        comments_positive = len(df.loc[df['Оценка'] >= 1])
        comments_negative = len(df.loc[df['Оценка'] <= -1])
        comments_valuable = len(df.loc[df['Оценка'] >= self.valuable_comments_score])
        comments_invaluable = len(df.loc[df['Оценка'] <= self.invaluable_comments_score])
        comments_convertion_valuable = int(100*comments_valuable/comments_total)
        comments_convertion_invaluable = int(100*comments_invaluable/comments_total)
        comments_convertion_mvp = comments_convertion_valuable - comments_convertion_invaluable
        timestamp = str(datetime.today().strftime('%d.%m.%Y %H:%M:%S'))
        df = df.loc[(df['Оценка'] >= self.valuable_comments_score) | (df['Оценка'] <= self.invaluable_comments_score)]
        df = df.sort_values(by=['Оценка'], ascending=False)
        tokenizer = RegexTokenizer()
        tokens = tokenizer.split('всё очень плохо')
        model = FastTextSocialNetworkModel(tokenizer=tokenizer)
        df.insert(1, 'Негатив', '0'); df.insert(2, 'Позитив', '0')
        for i, row in df.iterrows():
            score = self.analize_emotion(model, df.at[i, 'Текст'])
            df.at[i, 'Негатив'] = score[0]; df.at[i, 'Позитив'] = score[1]
        comments_convertion_tone = f'''{int(df['Негатив'].sum())}:{int(df['Позитив'].sum())}'''
        header = r'<!DOCTYPE html>'+ '\n' + '<html>' + '\n' + '<head>' + '\n' + \
        '<meta http-equiv="content-type" content="text/html; charset=utf-8" />' + \
        '\n' + '<title>' + self.title + '</title>' + '\n' + '</head>' + '\n' + \
        '<style>a {text-decoration: none;} </style>' + '\n'
        content = f'{header}<body style="font-family:Arial">\n<b>{self.title}</b><br><br> \
            Высказал за последнее время своё мнение около {comments_total} раз, \
            из них оценили хоть как-то {comments_positive} ответов и заминусовали {comments_negative}, \
            при этом реальную пользу принесли {comments_valuable} коммента ({comments_convertion_valuable}%), \
            а откровенным бредом были {comments_invaluable} коммента ({comments_convertion_invaluable}%), \
            включая:<br><br> \
            {df.to_html(index=False, render_links=True, escape=False)}<br><br> \
            Таким образом, индекс полезности данного персонажа по состоянию на {timestamp} \
            составляет {comments_convertion_mvp}%,<br><br>\
            при этом его настрой можно охарактеризовать как соотношение {comments_convertion_tone} явного негатива и позитива в суждениях, соответственно.<br><br>\
            А вот и его самые любимые слова (указывают на черты характера этого персонажа):<br><br> {frequency_analysis.to_html(index=False)}'
        with codecs.open(f'{self.name}.html', 'w', 'utf-8') as f:
            f.write(content)
        webbrowser.open(f'{self.name}.html')

    def run(self, mode=1):
        if mode == 0: # mode 0: download & analize
            self.download_data()
        if mode >= 0: # mode 1: analize only
            self.analize_data()

patterns = RecordPattern(
    control = 'Sergei Timofeyev',
    record  = '//div[@class="feed__item l-island-round"]',
    url     = './/a[@class="profile_comment_favorite__date t-link"]',
    date    = './/time[@class="time"]//text()',
    title   = './/a[@class="profile_comment_favorite__title"]//text()',
    text    = './/span[@class="profile_comment_favorite__text__full"]//text()',
    score   = './/div[@class="vote__value t-ff-1-500 l-fs-14 l-va-middle"]//text()'
)
url='https://vc.ru/u/174309-sergei-timofeyev/comments'
res = Resource(patterns=patterns, title='Тимофеев на VC', name='vc', url=url)
res.run(1)
