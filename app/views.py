from django.shortcuts import render

from django.views.generic import View

import pandas as pd
from .models import News

import os

import re
import numpy as np

import sqlalchemy
from sqlalchemy import Table
import sqlite3

dirname = os.path.dirname(__file__)


def to_sqlite(data):
    engine = sqlalchemy.create_engine('sqlite:///../db.sqlite3')
    conn  = sqlite3.connect('../db.sqlite3')
    # print(data)
    conn.execute("""
                        DELETE FROM app_news
                        """
    )
    conn.commit()
    data.to_sql('app_news', con=engine, if_exists='append', index=False)


def get_text(text):
    p = re.compile('(<.*?>)|([[^\.\w\s]])')
    return p.sub('', text)

def get_array(text):
    return np.array(text)

def read_csv():
    data = pd.read_csv(os.path.join(dirname, 'news.csv'), header=None,)
    data.columns = ['title', 'time', 'text']
    data = data[:10]
    # data['text'] = data['text'].apply(get_text)
    # data = open(os.path.join(dirname, 'news.csv'))
    # print(data.read())
    # return to_sqlite(data)
    to_sqlite(data)

class ParserView(View):
    def get(self, request):
        data = News.objects.all()
        return render(request, 'app/index.html', context={
            'data': data,
            })

class BodyView(View):
    def get(self, request, id):
        print('-------------')
        print(id)
        print('----------------')
        data = News.objects.get(id = id)

        return render(request, 'app/data.html', context={
            'text': text
        })


if __name__ == "__main__":
    read_csv()
