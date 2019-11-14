from django.shortcuts import render, get_object_or_404

from django.views.generic import View

import pandas as pd
from .models import News

import os

import re
import numpy as np

import sqlalchemy
from sqlalchemy import Table
import sqlite3

from django.core.paginator import Paginator



class ParserView(View):
    def get(self, request):
        data = News.objects.all()
        paginator = Paginator(data, 10)

        page_number = request.GET.get('page', 1)

        page = paginator.get_page(page_number)

        is_paginator = page.has_other_pages()

        if page.has_previous():
            prev_url = '?page={}'.format(page.previous_page_number())
        else:
            prev_url = ''

        if page.has_next():
            next_url = '?page={}'.format(page.next_page_number())
        else:
            next_url = ''

        return render(request, 'app/index.html', context={
            'page': page,
            'is_paginator': is_paginator,
            'prev_url': prev_url,
            'next_url': next_url
            })

class BodyView(View):
    def get(self, request, slug):
        body = get_object_or_404(News, id__iexact=slug)
        return render(request, 'app/data.html', context={'body': body}) 
