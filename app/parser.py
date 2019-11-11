from bs4 import BeautifulSoup
import requests

from random import choice
from time import sleep, time
import random

from multiprocessing import Pool
import json
import os
import csv

dirname = os.path.dirname(__file__)

class Helper:
    def __init__(self):
        self.proxies = None
        self.useragents = None

    def init(self):
        print('__init__')
        with open(os.path.join(dirname, 'news.csv'), 'w') as file:
            csv.writer(file)
            # writer.writerow((''))

    def get_proxy_list(self):
        self.proxies = open('txt_file/proxies.txt').read().split('\n')

    def get_user_a_list(self):
        self.useragents = open('txt_file/useragents.txt').read().split('\n')

    def get_html(self, url):
        proxy = {
            'http': 'http://{}'.format(choice(self.proxies)),
            }
        useragent = {
            'User-Agent': choice(self.useragents)
        }
        html = requests.get(url, headers=None, proxies=None).text
        return html

    def get_soup(self, html):
        soup = BeautifulSoup(html, features='html.parser')
        return soup

    def get_last_number(self):
        print('get_last_number')
        url = 'https://pasmi.ru/cat/news/'
        soup = self.get_soup(self.get_html(url))
        self.last_number = soup.find_all('a', class_='page-numbers')[1].text.strip()
    
    def get_all_links(self):
        print('get_all_links')
        self.all_links = ['https://pasmi.ru/cat/news/page/{}/'.format(i) for i in range(1, int(self.last_number)+1)]
    
    def get_news(self, link):      
        soup = self.get_soup(self.get_html(link))
        arts = soup.find_all('article')
        
        for art in arts:
            links_news = {}
            try:
                title = art.find('a', class_='entry-title').text.strip()
                href = art.find('a', class_='entry-title').get('href')
                time = art.find('span', class_='time').text.strip()
        
                soup_page = self.get_soup(self.get_html(href))
                text_page = [i for i in soup_page.find('div', class_='content').find_all('p')]

                links_news['title'] = title
                links_news['time'] = time
                links_news['text'] = text_page
                print('text is yes')
            except:
                links_news['title'] = ''
                links_news['time'] = ''
                links_news['text'] = ['']

            self.write_csv(links_news)
    
    # def save_to_json(self):
    #     print(self.links_news)
    #     with open(os.path.join(dirname, 'respons.json'), 'w') as f:
    #         json.dump(self.links_news, f, indent=2, ensure_ascii=False)
    
    def write_csv(self, data):
        with open(os.path.join(dirname, 'news.csv'), 'a') as file:
            writer = csv.writer(file)
            writer.writerow((data['title'], data['time'], data['text']))

def main():
    helper = Helper()

    helper.init()

    helper.get_last_number()
    helper.get_all_links()

    with Pool(10) as p:
        p.map(helper.get_news, helper.all_links)

    # for number, link in enumerate(helper.all_links):
    #     print(number)
    #     helper.get_news(link)


# --------------------------------------------------

import asyncio
import aiohttp


def save_to_file(data):
    with open(os.path.join(dirname, 'news.csv'), 'a') as file:
            writer = csv.writer(file)
            writer.writerow((data['title'], data['time'], data['text']))

async def get_response(url, session):
    async with session.get(url) as response:
        print(response.status)
        return await response.text()

async def fetch_content(url, session):
    data = await get_response(url, session)
    soup = BeautifulSoup(data, features='html.parser')
    arts = soup.find_all('article')
    for art in arts:
        links_news = {}
        try:
            title = art.find('a', class_='entry-title').text.strip()
            href = art.find('a', class_='entry-title').get('href')
            time = art.find('span', class_='time').text.strip()

            data_page = await get_response(href, session)
            soup_page = BeautifulSoup(data_page, features='html.parser')
            text_page = [i for i in soup_page.find('div', class_='content').find_all('p')]

            links_news['title'] = title
            links_news['time'] = time
            links_news['text'] = text_page

        except:
            links_news['title'] = ''
            links_news['time'] = ''
            links_news['text'] = ['']

        save_to_file(links_news)

async def main2():
    helper = Helper()

    helper.get_last_number()
    helper.get_all_links()

    tasks = []

    async with aiohttp.ClientSession() as session:
        for url in helper.all_links:
            task = asyncio.create_task(fetch_content(url, session))
            tasks.append(task)
        
        await asyncio.gather(*tasks)

    save_to_json(data=links_news)

if __name__ == "__main__":
    t0 = time()
    # asyncio.run(main2())
    main()
    print(time()-t0)
    # main()