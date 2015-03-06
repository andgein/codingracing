__author__ = 'Andrew Gein <andgein@yandex.ru>'

from django.shortcuts import render


def index(request):
    return render(request, 'index.html')


def training(request):
    pass

