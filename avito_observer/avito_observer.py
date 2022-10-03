import sys
import os
from dataclasses import dataclass
from datetime import datetime
from lxml import html
import urllib.request
import hashlib
##import codecs
import configparser

assert sys.version_info >= (3,7)

## запись
@dataclass(order=True)
class Record:
    title: str = '' ## заголовок
    text: str = ''  ## текст
    link: str = ''  ## адрес
    date: str = ''  ## дата
    price: str = '' ## стоимость
    crc: str = ''   ## контрольная сумма
    ## подсчет контрольной суммы (text + title + price) -- отпечаток записи
    def check(self):
        self.crc = hashlib.sha256((f'{self.text}{self.title}{self.price}').encode()).hexdigest()
        return self.crc
    ## просмотр записи
    def view(self):
        print(f'{"-"*80}\n{self.text}\n{self.title}\n{self.price}\n\n{self.link}\n{"-"*80}\n')

## шаблон
class Template:
    name: str = ''          ## наименование шаблона
    target: str = ''        ## целевой адрес страницы
    common: str = ''        ## шаблон блока страницы с записями
    title: str = ''         ## шаблон заголовка записи
    text: str = ''          ## шаблон текста записи
    link: str = ''          ## шаблон адреса записи
    date: str = ''          ## шаблон даты записи
    price: str = ''         ## шаблон стоимости
    records: Record = []    ## новые записи (полный формат, class Record)
    fingerprints: str = []  ## существующие записи (отпечатки, только КС)
    config_file: None       ## файл шаблона
    config_parser: None     ## парсер шаблона

    ## инициализация ядра
    def __init__(self, config_file: str):
        ## загрузка шаблона из файла ini        
        self.config_file = config_file
        self.config_parser = configparser.RawConfigParser(allow_no_value=True)
        self.config_parser.read(self.config_file)
        self.name = str(self.config_parser.get('TEMPLATE', 'name'))
        self.target = str(self.config_parser.get('TEMPLATE', 'target'))
        self.common = str(self.config_parser.get('TEMPLATE', 'common'))
        self.title = str(self.config_parser.get('TEMPLATE', 'title'))
        self.price = str(self.config_parser.get('TEMPLATE', 'price'))
        self.date = str(self.config_parser.get('TEMPLATE', 'date'))
        self.link = str(self.config_parser.get('TEMPLATE', 'link'))
        ## загрузка отпечатков (КС) обработанных записей
        self.fingerprints = list(key for key, value in self.config_parser.items('CRCS'))
    ## сканирование объекта
    def scan(self):
        ## вывод наименования шаблона
        print(f'{80*"*"}\ntemplate: "{self.name}"')
        ## вывод времени предыдущего запуска
        print(f'last runned: {str(self.config_parser.get("PROPERTIES", "datetime"))}\n{80*"*"}\n')         
        ## запрос объекта
        with urllib.request.urlopen(self.target) as response:
            content = response.read().decode()
        ## демо-режим объекта
##        with open('demo.html', 'r', encoding='utf8') as demo:
##            content = demo.read()
        ## распознавание записей по шаблону
        items = html.fromstring(content).xpath(self.common)
        print(f'found total: {len(items)} records')
        for item in items:
            self.records.append(Record(
                title = item.xpath(self.title)[0],
                price = item.xpath(self.price)[0],                
                date = item.xpath(self.date)[0],
                link = item.xpath(self.link)[0].get('href')))
        counter = 0
        for record in self.records:
            ## если запись новая/изменена: вывод на экран и сохранение отпечатка
            if not record.check() in self.fingerprints:
                record.view()
                self.fingerprints.append(record.crc)
                counter += 1
        ## вывод результата
        print(f'recent/modified: {counter} records\n\npress any key to save current configuration / marks all as readed...')
        input()
        ## сохранение отпечатков записей в файл шаблона
        self.config_parser.set('PROPERTIES', 'datetime', str(datetime.today().strftime('%d.%m.%Y %H:%M')))
        for item in self.fingerprints:
            self.config_parser.set('CRCS', item, None)
        with open(self.config_file, 'w') as configfile:
            self.config_parser.write(configfile)

## ядро
class Core:
    templates: Template = []        ## шаблоны
    def __init__(self, templates=[]):
        ## если не переданы имена файлов-шалонов, использовать все *.ini рядом
        if templates == []:
            templates = list(file for file in os.listdir() if file.endswith('.ini'))
        for template in templates:
            self.templates.append(Template(template))
    ## запуск основного процесса
    def run(self):
        for template in self.templates:
            template.scan()

core = Core()
core.run()
