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



class ParserView(View):
    def get(self, request):
        data = News.objects.all()
        return render(request, 'app/index.html', context={
            'data': data,
            })

class BodyView(View):
    pass
    # def get(self, request, id):
    #     print('-------------')
    #     print(id)
    #     print('----------------')
    #     data = News.objects.get(id = id)

    #     return render(request, 'app/data.html', context={
    #         'text': text
    #     })


if __name__ == "__main__":
    read_csv()
