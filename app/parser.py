from bs4 import BeautifulSoup
import requests

from random import choice
from time import sleep, time
import random

from multiprocessing import Pool
import json
import os
import csv
import pandas as pd

import re
import numpy as np

import sqlalchemy
from sqlalchemy import Table
import sqlite3

dirname = os.path.dirname(__file__)

class Helper:
    def __init__(self):
        self.proxies = None
        self.useragents = None

    def init(self, name='news'):
        print('__init__')
        with open(os.path.join(dirname, '{}.csv'.format(name)), 'w') as file:
            csv.writer(file)

    def get_proxy_list(self):
        self.proxies = open('txt_file/proxies.txt').read().split('\n')

    def get_user_a_list(self):
        self.useragents = open('txt_file/useragents.txt').read().split('\n')

    def get_html(self, url):
        print('get_html')
        self.get_proxy_list()
        self.get_user_a_list()
        proxy = {
            'http': 'http://{}'.format(choice(self.proxies)),
            }
        useragent = {
            'User-Agent': choice(self.useragents)
        }
        html = requests.get(url, headers=None, proxies=None).text
        return html

    def get_soup(self, html):
        print('get_soup')
        soup = BeautifulSoup(html, features='html.parser')
        return soup

    def get_last_number(self):
        print('get_last_number')
        url = 'https://pasmi.ru/cat/news/'
        # url = 'https://pasmi.ru/cat/news/page/2/'
        soup = self.get_soup(self.get_html(url))
        print(soup)
        # self.last_number = soup.find_all('a', class_='page-numbers')[1].text.strip()
    
    def take_all_hrefs(self):
        self.href_list = []
        date_dict = {
            'month_2000': ['aug', 'sep', 'oct', 'nov', 'dec'],
            'month': [ 'jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug', 'sep', 'oct', 'nov', 'dec'],
            'day': [str(i) for i in range(1, 32)],
            'yers': [str(i) for i in range(2000, 2020)]
        }
        for yers in date_dict['yers']:
            if yers == '2000':
                for month in date_dict['month_2000']:
                    for day in date_dict['day']:
                        self.href_list.append(
                            'https://www.newsru.com/allnews/{}{}{}/'.format(
                                day, month, yers
                            )
                        )
            for month in date_dict['month']:
                for day in date_dict['day']:
                    self.href_list.append(
                        'https://www.newsru.com/allnews/{}{}{}/'.format(
                            day, month, yers
                        )
                    )
        print(len(self.href_list))


    
    def get_all_links(self):
        print('get_all_links')
        self.all_links = ['https://pasmi.ru/cat/news/page/{}/'.format(i) for i in range(1, int(self.last_number)+1)]
    
    def get_all_href(self, link):
        print('get_all_href')
        soup = self.get_soup(self.get_html(link))
        arts = soup.find_all('article')
        for art in arts:
            links_news = {}
            try:
                href = art.find('a', class_='entry-title').get('href')
                links_news['href'] = href
            except:
                links_news['href'] = ''

            self.write_csv(data=links_news, name='hrefs')
    
    def get_news(self, link):
        soup = self.get_soup(self.get_html(link[0])) 
        try:
            links_news = {}
            content = soup.find('div', class_='entry-content')
            title = content.find('h1', class_='entry-title').text.strip()
            time = content.find('span', class_='time').text.strip()
            text = [i.text.strip() for i in content.find('div', class_='content').find_all('p')]

            links_news['title'] = title
            links_news['time'] = time
            links_news['text'] = text

            self.write_csv(data=links_news, name = 'news')
        except:
            print('Error')
    
    # def save_to_json(self):
    #     print(self.links_news)
    #     with open(os.path.join(dirname, 'respons.json'), 'w') as f:
    #         json.dump(self.links_news, f, indent=2, ensure_ascii=False)
    
    def write_csv(self, data, name):
        print('save_to_file')
        with open(os.path.join(dirname, '{}.csv'.format(name)), 'a') as file:
            writer = csv.writer(file)
            if name == 'hrefs':
                writer.writerow((data['href'],))
            writer.writerow((data['title'], data['time'], data['text']))

    def to_sqlite(self, data):
        print('to_sqlite')
        engine = sqlalchemy.create_engine('sqlite:///../db.sqlite3')
        data.to_sql('app_news', con=engine, if_exists='append', index=False)

    def clear_db(self):
        print('clear databases')
        conn  = sqlite3.connect('../db.sqlite3')
        conn.execute("""
                        DELETE FROM app_news
                    """
                    )
        conn.commit()

    def read_csv(self):
        print('read_csv')
        data = pd.read_csv(os.path.join(dirname, 'news.csv'), header=None,)
        data.columns = ['title', 'time', 'text']
        data = data.dropna(0)
        data = data[:3000]
        # data['text'] = data['text'].apply(get_text)
        # data = open(os.path.join(dirname, 'news.csv'))
        self.to_sqlite(data)

    def get_text(self, text):
        p = re.compile('(<.*?>)|([[^\.\w\s]])')
        return p.sub('', text)

    def get_array(self, text):
        return np.array(text)


def main():
    helper = Helper()

    # helper.init(name='news')

    # helper.take_all_hrefs()

    # helper.get_last_number()
    # helper.get_all_links()

    # with Pool(50) as p:
    #     p.map(helper.get_all_href, helper.all_links)

    # hrefs = pd.read_csv(os.path.join(dirname, 'hrefs.csv'), header=None).values
    
    # with Pool(200) as p:
    #     p.map(helper.get_news, hrefs)

    # for number, link in enumerate(helper.all_links):
    #     print(number)
    #     helper.get_news(link)

    helper.clear_db()
    helper.read_csv()


# --------------------------------------------------

import asyncio
import aiohttp

def save_hrefs(data):
    print('save_hrefs')
    with open(os.path.join(dirname, 'hrefs.csv'), 'a') as file:
        writer = csv.writer(file)
        writer.writerow((data['href'],))

def save_to_file(data):
    print('save_to_file')
    with open(os.path.join(dirname, 'news.csv'), 'a') as file:
        writer = csv.writer(file)
        writer.writerow((data['title'], data['time'], data['text']))

async def get_response(url, session):
    async with session.get(url) as response:
        print(response.status)
        return await response.text()


async def news_content(url, session):
    data = await get_response(url, session)
    links_news = {}
    text = ' \n'
    try:
        soup = BeautifulSoup(data, features='html.parser')
        # content = soup.find('div', class_='entry-content')
        # title = content.find('h1', class_='entry-title').text.strip()
        # time = content.find('span', class_='time').text.strip()
        # text = [i.text.strip() for i in content.find('div', class_='content').find_all('p')]
        content = soup.find('div', class_='article')
        title = content.find('h1', class_='article-title').text.strip()
        time = content.find('div', class_='article-date').text.strip()
        text_list= [i.text.strip() for i in content.find('div', class_='article-text').find_all('p')]

        links_news['title'] = title
        links_news['time'] = time
        links_news['text'] = text_list
    except:
        print('Error')
        links_news['title'] = ''
        links_news['time'] = ''
        links_news['text'] = ''
    save_to_file(links_news)

# async def fetch_content(url, session):
#     data = await get_response(url, session)
#     soup = BeautifulSoup(data, features='html.parser')
#     arts = soup.find_all('article')
#     links_news = {}
#     for art in arts:
#         try:
#             href = art.find('a', class_='entry-title').get('href')
#             links_news['href'] = href
#         except:
#             links_news['href'] = ''
#         save_hrefs(links_news)

async def fetch_content_href(url, session):
    data = await get_response(url, session)
    soup = BeautifulSoup(data, features='html.parser')
    hrefs = soup.find_all('a', class_='index-news-title')
    links_news = {}
    for href in hrefs:
        try:
            links_news['href'] = 'https://www.newsru.com{}'.format(href.get('href'))
        except:
            links_news['href'] = ''
        save_hrefs(links_news)
    

    # tasks = []
    # async with aiohttp.ClientSession() as session:
    #     for url in list_href:
    #         task = asyncio.create_task(news_content(url, session))
    #         tasks.append(task)
        
    #     await asyncio.gather(*tasks)

    # for art in arts:
    #     links_news = {}
    #     try:
    #         title = art.find('a', class_='entry-title').text.strip()
    #         href = art.find('a', class_='entry-title').get('href')
    #         time = art.find('span', class_='time').text.strip()

    #         soup_page = helper.get_soup(helper.get_html(href))
    #         text_page = [i for i in soup_page.find('div', class_='content').find_all('p')]

    #         links_news['title'] = title
    #         links_news['time'] = time
    #         links_news['text'] = text_page

    #     except:
    #         links_news['title'] = ''
    #         links_news['time'] = ''
    #         links_news['text'] = ['']

    #     save_to_file(links_news)

async def main2(dir_):
    helper = Helper()

    # helper.init(name='news')

    # helper.get_last_number()
    # helper.get_all_links()
    # helper.take_all_hrefs()

    # tasks = []

    # async with aiohttp.ClientSession() as session:
    #     for url in helper.all_links:
    #         task = asyncio.create_task(fetch_content(url, session))
    #         tasks.append(task)      
    #     await asyncio.gather(*tasks)


    # tasks = []
    # async with aiohttp.ClientSession() as session:
    #     for url in helper.href_list:
    #         task = asyncio.create_task(fetch_content_href(url, session))
    #         tasks.append(task)       
    #     await asyncio.gather(*tasks)

    hrefs = pd.read_csv(os.path.join(dirname, 'hrefs.csv'), header=None).values
    tasks = []
    async with aiohttp.ClientSession() as session:
        for url in hrefs[dir_[0]:dir_[1]]:
            task = asyncio.create_task(news_content(url[0], session))
            tasks.append(task)    
        await asyncio.gather(*tasks)

def init_main(main):
    asyncio.run(main2(main))

if __name__ == "__main__":
    t0 = time()
    main()
    # list_ = []
    # n = 21300
    # while n>0:
    #     a = n-200
    #     if a<0:
    #         list_.append([0, n])
    #         break
    #     list_.append([a, n])
    #     n=a
    # print(list_)
    # with Pool(4) as p:
    #     p.map(init_main, list_)
    # for i in list_:
    #     print(i)
    # asyncio.run(main2([0, 100]))
    
    print(time()-t0)
    # main()