from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader
from random import random

import datetime


def index(request):
    context = {
        'generic_var': random()
    }

    return render(request, 'index.html', context)


def current_datetime(request):
    now = datetime.datetime.now()
    html = "<html><body>It is now %s.</body></html>" % now
    return HttpResponse(html)
