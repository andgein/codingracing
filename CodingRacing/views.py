from django.templatetags.i18n import language

__author__ = 'Andrew Gein <andgein@yandex.ru>'

from django.shortcuts import render
import django.http

import CodingRacing.models as models
from datetime import datetime


def index(request):
    return render(request, 'index.html')


def training(request):
    return render(request, 'training.html')


def training_start(request):
    lang = request.GET.get('lang')
    client_time = request.GET.get('timestamp')

    if lang is None or client_time is None:
        return django.http.HttpResponseBadRequest()
    if lang not in models.LANGUAGES.keys():
        return django.http.HttpResponseBadRequest('Invalid language')
    try:
        client_time = int(client_time)
        assert(client_time > 0)
        client_time = datetime.utcfromtimestamp(client_time)
    except ValueError or AssertionError or TypeError:
        return django.http.HttpResponseBadRequest('Invalid timestamp')

    user = models.User.objects.get(vk_id=1)
    game = models.TrainingGame(user=user, language=lang, start_client_time=client_time)
    game.save()

    return django.http.JsonResponse({'lang': game.language, 'start_time': game.start_time})