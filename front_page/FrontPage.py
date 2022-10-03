from dataclasses import dataclass, field
import webbrowser
import codecs
import os
from selenium import webdriver
from selenium.webdriver.edge.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium import webdriver
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from selenium.webdriver.remote.remote_connection import LOGGER
import logging
from selenium.webdriver.remote.remote_connection import LOGGER as seleniumLogger
seleniumLogger.setLevel(logging.ERROR)
from urllib3.connectionpool import log as urllibLogger
urllibLogger.setLevel(logging.ERROR)
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)10s: %(message)s',
                    datefmt='%d.%m.%Y %H:%M:%S',
                    filename='FrontPage.log',
                    filemode='w')
log = logging.getLogger('FrontPage')

@dataclass
class Resource():
    name: str = ''
    url: str = ''
    base_url: str = ''
    pattern_block: str = ''
    pattern_items: str = ''
    pattern_title: str = ''
    pattern_link: str = ''
    data: dict = field(default_factory=dict)
    image: str = ''

def preview(resources):
    content = ''
    for res in resources:
        content += f'<h1>{res.name}</h1>'
        for link, title in res.data.items():
            content += f'<a href="{link}">{title}</a></br>'
        if res.image:
            content += f'<p><img src="data:image/jpeg;base64,{res.image}" /></p>'
    filename = 'FrontPage.html'
    content = r'<!DOCTYPE html>'+ '\n' + '<html>' + '\n' + '<head>' + '\n' + \
    '<meta http-equiv="content-type" content="text/html; charset=utf-8" />' + \
    '\n' + '<title>' + filename + '</title>' + '\n' + '</head>' + '\n' + \
    '<style>a {text-decoration: none;} </style>' + '\n' + \
    '<body style="font-family:Arial">' + '\n' + content + '\n' + '</body>' + \
    '\n' + '</html>'
    with codecs.open(filename, 'w', 'utf-8') as f:
        f.write(content)
    webbrowser.open(filename)

def download(resources):
    options = Options()
    options.add_argument("--headless")
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    driver = webdriver.Edge(EdgeChromiumDriverManager().install(), options=options, service_log_path='NUL')
    os.environ['WDM_LOG_LEVEL'] = '0'
    for res in resources:
        try:
            print(f'{res.name} processing...')
            log.info(f'{res.name} processing...')
            driver.get(res.url)
            log.debug(f'page loading and news block identification...')
            WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, res.pattern_block)))
            log.debug(f'{res.url} loaded OK')
            log.debug(f'block identification...')
            block = driver.find_element(By.XPATH, res.pattern_block)
            log.debug(f'block identificated')
            log.debug(f'block screenshoting...')
            # try:
            #     res.image = block.screenshot_as_base64
            #     log.debug(f'block screenshoted')
            # except Exception as inst:
            #     log.warning(f'{type(inst)} {inst.args} {inst}')
            log.debug(f'items identification...')
            items = block.find_elements(By.XPATH, res.pattern_items)
            log.debug(f'identified items: {len(items)}')
            for item in items:
                log.debug(f'title identification...')
                news_title = item.find_element(By.XPATH, res.pattern_title).text
                log.debug(f'{news_title}')
                log.debug(f'link identification...')
                news_link = item.find_element(By.XPATH, res.pattern_link).get_attribute('href')
                log.debug(f'{news_link}')
                news_link = res.base_url + news_link
                res.data[news_link] = news_title
            log.info(f'{res.name} completed successfully: {len(items)} items')
        except Exception as inst:
            log.error(f'{type(inst)} {inst.args} {inst}')
    driver.close()
    driver.quit()
    return resources

def main():
    resources = []
    with codecs.open('FrontPage.ini', 'r', 'utf-8') as f:
        resources = eval(f.read())
    resources = download(resources)
    preview(resources)
    with open('FrontPage.log') as f:
        print(f.read())

main()
