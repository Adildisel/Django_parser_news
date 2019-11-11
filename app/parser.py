from bs4 import BeautifulSoup
import requests

from random import choice
from time import sleep, time
import random

from multiprocessing import Pool
import json
import os

dirname = os.path.dirname(__file__)

class Helper:
    def __init__(self):
        self.r = ''
        self.ip = ''
        self.user_a = ''
        self.proxies = []
        self.useragents = []
        self.links_news = {}

    def get_html(self, url):
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
        print('get_news')
        
        soup = self.get_soup(self.get_html(link))
        arts = soup.find_all('article')
        for art in arts:
            try:
                art_id = art.get('id')
                print(art_id)
                # art_id = 'Data'
                # title = art.find('a', class_='entry-title').text.strip()
                href = art.find('a', class_='entry-title').get('href')
                # time = art.find('span', class_='time').text.strip()

                self.links_news[art_id] = {}
                # self.links_news[art_id]['title'] = title
                self.links_news[art_id]['href'] = href
                # self.links_news[art_id]['time'] = time
            except:
                art_id = 'None'              
                self.links_news[art_id] = {}
                # self.links_news[art_id]['title'] = ''
                self.links_news[art_id]['href'] = ''
                # self.links_news[art_id]['time'] = ''
        # print(self.links_news)
    
    def save_to_json(self):
        print('save_to_json')
        with open(os.path.join(dirname, 'respons.json'), 'w') as f:
            json.dump(self.links_news, f, indent=2, ensure_ascii=False)

def main():
    helper = Helper()

    url = 'http://sitespy.ru/my-ip'
    url_news = ''

    helper.get_last_number()
    helper.get_all_links()

    with Pool(40) as p:
        p.map(helper.get_news, helper.all_links)

    # for number, link in enumerate(helper.all_links):
    #     print(number)
    #     helper.get_news(link)

    helper.save_to_json()


# --------------------------------------------------

import asyncio
import aiohttp

links_news = {}

async def save_to_json(links_news):
    with open(os.path.join(dirname, 'respons.json'), 'w') as f:
        json.dump(links_news, f, indent=2, ensure_ascii=False)

async def get_json(url, session):
    async with session.get(url) as response:
        print(response.status)
        return await response.text()

# async def get_page(url, session):
#     async with session.get(url)


async def fetch_content(url, session):
    data = await get_json(url, session)
    soup = BeautifulSoup(data, features='html.parser')
    arts = soup.find_all('article')
    for art in arts:
        try:
            art_id = art.get('id')
            print(art_id)
            # art_id = 'Data'
            # title = art.find('a', class_='entry-title').text.strip()
            href = art.find('a', class_='entry-title').get('href')
            # time = art.find('span', class_='time').text.strip()

            # data_page = await get_json(href, session)
            # soup_page = BeautifulSoup(data_page, features='html.parser')
            # text_page = [i for i in soup_page.find('div', class_='content').find_all('p')]
            # print(text_page)

            # links_news[art_id] = {}
            # links_news[art_id]['title'] = title
            links_news[art_id]['href'] = href
            # links_news[art_id]['time'] = time
            # links_news[art_id]['text'] = text_page

        except:
            art_id = 'None'              
            links_news[art_id] = {}
            # links_news[art_id]['title'] = ''
            links_news[art_id]['href'] = ''
            # links_news[art_id]['time'] = ''
            # links_news[art_id]['text'] = ['']
    save_to_json(links_news)


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

    # await save_to_json()

    # save_to_json()

if __name__ == "__main__":
    t0 = time()
    asyncio.run(main2())
    # main()
    print(time()-t0)
    # main()