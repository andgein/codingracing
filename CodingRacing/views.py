import os

from CodingRacing import code_database
import ImageGenerator


__author__ = 'Andrew Gein <andgein@yandex.ru>'

from django.shortcuts import render, get_object_or_404
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
    if lang not in code_database.LANGUAGES.keys():
        return django.http.HttpResponseBadRequest('Invalid language')
    try:
        client_time = int(client_time)
        assert (client_time > 0)
        client_time = datetime.utcfromtimestamp(client_time)
    except (ValueError, AssertionError, TypeError):
        return django.http.HttpResponseBadRequest('Invalid timestamp')

    user = models.User.objects.get(vk_id=1)
    code = code_database.get_code(lang)
    game = models.TrainingGame(user=user, language=lang, start_client_time=client_time, text=code)
    game.save()

    return django.http.JsonResponse({'id': game.id,
                                     'lang': game.language,
                                     'start_time': game.start_time,
                                     'image': '/training/%d/code.png' % game.id})


def training_code(request, game_id):
    game_id = int(game_id)
    game = get_object_or_404(models.TrainingGame, id=game_id)
    # TODO: check time for game

    os.makedirs('codes-images/training', exist_ok=True)

    filename = 'codes-images/training/%d.png' % game.id
    if not os.path.exists(filename):
        ImageGenerator.generate(game.text).save(filename)
    with open(filename, 'rb') as f:
        return django.http.HttpResponse(f.read(), content_type='image/png')


def training_update(request, game_id):
    game_id = int(game_id)
    game = get_object_or_404(models.TrainingGame, id=game_id)

    current_text = request.POST.get('text')
    if current_text is None:
        return django.http.HttpResponseBadRequest()

    game.last_text = current_text
    game.save()

    diff_position = code_database.find_diff_position(game.text, game.last_text)
    return django.http.JsonResponse({'success': True, 'diff_position': diff_position})


def training_finish(request, game_id):
    game_id = int(game_id)
    game = get_object_or_404(models.TrainingGame, id=game_id)

    current_text = request.POST.get('text')
    if current_text is None:
        return django.http.HttpResponseBadRequest()

    client_time = request.POST.get('timestamp')
    try:
        client_time = int(client_time)
        assert (client_time > 0)
        client_time = datetime.utcfromtimestamp(client_time)
    except (ValueError, AssertionError, TypeError):
        return django.http.HttpResponseBadRequest('Invalid timestamp')

    game.last_text = current_text
    game.state = 'finished'
    game.finish_time = datetime.now()
    game.finish_client_time = client_time
    game.save()
    return django.http.JsonResponse({'success': True})