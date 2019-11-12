from django.shortcuts import render

from django.views.generic import View

from .parser import Helper

import pandas as pd


def read_csv():
    data = pd.read_csv('news.csv')
    print(data.head())

class ParserView(View):
    def get(self, request):
        data = 'Name'
        return render(request, 'app/index.html', context={'data': data})


if __name__ == "__main__":
    read_csv()
