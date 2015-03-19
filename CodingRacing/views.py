# -*- coding: utf-8 -*-
from cgitb import enable

__author__ = 'Andrew Gein <andgein@yandex.ru>'

from datetime import datetime, timedelta
import os
import random
import requests
import string

from CodingRacing import code_database
import ImageGenerator
import CodingRacing.models as models
import CodingRacing.decorators as decorators
import CodingRacing.local_settings as local_settings

from django.shortcuts import render, get_object_or_404
from django.views.decorators.csrf import ensure_csrf_cookie
import django.http
import django.db
import django.db.models
from django.template.defaulttags import register


@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)


def generate_password(length=4):
    return ''.join([random.choice(string.digits) for _ in range(length)])


@ensure_csrf_cookie
def index(request):
    user = decorators.get_user_by_request(request)
    context = {'is_auth': bool(user),
               'vk_redirect_url': local_settings.VK_REDIRECT_URL}
    if context['is_auth']:
        context['user'] = user
    return render(request, 'index.html', context)


def auth_user(response, user):
    response.set_cookie('vk_id', user.vk_id)
    response.set_cookie('auth', decorators.get_auth_cookie(user.vk_id))


# TODO: check state
def auth(request):
    if 'code' not in request.GET:
        return django.http.JsonResponse({'error': request.GET.get('error_description', 'unknown')})
    code = request.GET['code']
    access_token_url = 'https://oauth.vk.com/access_token?client_id=%d&client_secret=%s&code=%s&redirect_uri=%s' % (
        local_settings.VK_APP_ID,
        local_settings.VK_APP_SECRET,
        code,
        local_settings.VK_REDIRECT_URL
    )
    vk_answer = requests.get(access_token_url).json()
    if 'access_token' not in vk_answer:
        return django.http.JsonResponse({'error': vk_answer.get('error_description', 'unknown')})
    access_token = vk_answer['access_token']

    getuser_url = 'https://api.vk.com/method/users.get?fields=city,photo_50,occupation&access_token=%s&v=5.29' % access_token
    vk_answer = requests.get(getuser_url).json()
    if 'response' not in vk_answer:
        return django.http.JsonResponse({'error': 'Can\'t retrieve information about you from VK'})
    user_info = vk_answer['response'][0]

    response = django.http.HttpResponseRedirect('/')
    try:
        user = models.User.objects.get(vk_id=user_info['id'])
        auth_user(response, user)
    except models.User.DoesNotExist:
        new_user = models.User()
        new_user.vk_id = user_info['id']
        new_user.first_name = user_info['first_name']
        new_user.last_name = user_info['last_name']
        new_user.photo_50 = user_info['photo_50']
        new_user.city = user_info['city']['title']
        new_user.save()
        auth_user(response, new_user)

    return response


@decorators.auth_only
def logout(request):
    response = django.http.HttpResponseRedirect('/')
    response.set_cookie('vk_id', '')
    response.set_cookie('auth', '')
    return response


@ensure_csrf_cookie
@decorators.auth_only
def training(request):
    if 'lang' not in request.GET:
        return django.http.HttpResponseRedirect('/')
    return render(request, 'training.html')


@decorators.auth_only
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

    code = code_database.get_code(lang, 'training')
    game = models.TrainingGame(user=request.user, language=lang, start_client_time=client_time, text=code,
                               state='running')
    game.save()

    return django.http.JsonResponse({'id': game.id,
                                     'lang': game.language,
                                     'start_time': game.start_time,
                                     'image': '/training/%d/code.png' % game.id})


@decorators.auth_only
def training_code(request, game_id):
    game_id = int(game_id)
    game = get_object_or_404(models.TrainingGame, id=game_id)
    # TODO: check time for game

    if request.user.vk_id != game.user.vk_id:
        return django.http.HttpResponseBadRequest('Invalid game id')

    try:
        os.makedirs(os.path.join(local_settings.PROJECT_DIR, 'codes-images/training'), exist_ok=True)
    except TypeError:
        try:
            os.makedirs(os.path.join(local_settings.PROJECT_DIR, 'codes-images/training'))
        except:
            pass

    filename = os.path.join(local_settings.PROJECT_DIR, 'codes-images/training/%d.png' % game.id)
    if not os.path.exists(filename):
        ImageGenerator.generate(game.text).save(filename)
    with open(filename, 'rb') as f:
        return django.http.HttpResponse(f.read(), content_type='image/png')


@decorators.auth_only
def training_update(request, game_id):
    game_id = int(game_id)
    game = get_object_or_404(models.TrainingGame, id=game_id)

    if request.user.vk_id != game.user.vk_id:
        return django.http.HttpResponseBadRequest('Invalid game id')
    if game.state != 'running':
        return django.http.HttpResponseBadRequest('Game has been finished already')

    current_text = request.POST.get('text')
    if current_text is None:
        return django.http.HttpResponseBadRequest()

    last_text = models.LastText(user=request.user, game_type='training', game_id=game.id, last_text=current_text)
    last_text.save()

    diff_position = code_database.find_diff_position(game.text, current_text)

    # Decrement because we want to set cursor before error, not after
    if diff_position is not None:
        diff_position -= 1

    diff_position = code_database.get_row_and_column(current_text, diff_position)
    return django.http.JsonResponse({'success': True, 'diff_position': diff_position})


@decorators.auth_only
def training_finish(request, game_id):
    game_id = int(game_id)
    game = get_object_or_404(models.TrainingGame, id=game_id)

    if request.user.vk_id != game.user.vk_id:
        return django.http.HttpResponseBadRequest('Invalid game id')
    if game.state != 'running':
        return django.http.HttpResponseBadRequest('Game has been finished already')

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

    last_text = models.LastText(user=request.user, game_type='training', game_id=game_id, last_text=current_text)
    last_text.save()

    game.state = 'finished'
    game.finish_time = datetime.now()
    game.finish_client_time = client_time
    game.save()

    diff_position = code_database.find_diff_position(game.text, current_text)
    distance = code_database.levenshtein_distance(game.text, current_text)

    seconds = int((game.finish_client_time - game.start_client_time).total_seconds()) - local_settings.DELAY_GAME_START
    if seconds < 0:
        seconds = 0
    chars = len(game.text)
    total_seconds = seconds + distance * local_settings.LEVENSHTEIN_PENALTY
    speed = int((chars / total_seconds) * 60)

    return django.http.JsonResponse({'success': True,
                                     'diff_position': diff_position,
                                     'distance': distance,
                                     'speed': speed,
                                     'seconds': seconds,
                                     'total_seconds': '%d + %d x %d = %d' % (
                                         seconds, local_settings.LEVENSHTEIN_PENALTY, distance, total_seconds)})


@ensure_csrf_cookie
@decorators.auth_only
def contest(request):
    return render(request, 'contest.html')


@django.db.transaction.atomic
@decorators.auth_only
def contest_enjoy(request):
    password = request.POST.get('password', None)
    if password is None:
        return django.http.JsonResponse({'error': 'Password?'})

    games = models.ContestGame.objects.filter(password__iexact=password, state='not-started')
    if not games.exists():
        return django.http.JsonResponse({'error': 'Неверный пароль'})

    game = games[0]
    if game.users.count() == local_settings.MAX_USERS_IN_CONTEST:
        return django.http.JsonResponse({'error': 'Слишком много участников :('})

    game.users.add(request.user)
    game.save()

    return django.http.JsonResponse({'id': game.id,
                                     'lang': game.language})


@decorators.auth_only
def contest_check(request, game_id):
    game_id = int(game_id)
    game = get_object_or_404(models.ContestGame, id=game_id)
    if request.user not in game.users.all():
        return django.http.JsonResponse({'error': 'Invalid game id'})

    if game.start_time is None:
        game.start_time = datetime.now()
    before_start = game.start_time - datetime.now()
    return django.http.JsonResponse({'state': game.state,
                                     'before_start': int(before_start.total_seconds()),
                                     'image': '/contest/%d/code.png' % game_id,
    })


@decorators.auth_only
def contest(request, game_id):
    game = get_object_or_404(models.ContestGame, id=game_id)
    if request.user not in game.users.all():
        return django.http.HttpResponseBadRequest('Invalid game id')

    return render(request, 'contest.html')


@decorators.auth_only
def contest_code(request, game_id):
    game_id = int(game_id)
    game = get_object_or_404(models.ContestGame, id=game_id)
    # TODO: check time for game

    if request.user not in game.users.all():
        return django.http.HttpResponseBadRequest('Invalid game id')

    try:
        os.makedirs(os.path.join(local_settings.PROJECT_DIR, 'codes-images/contest'), exist_ok=True)
    except TypeError:
        try:
            os.makedirs(os.path.join(local_settings.PROJECT_DIR, 'codes-images/contest'))
        except:
            pass

    filename = os.path.join(local_settings.PROJECT_DIR, 'codes-images/contest/%d.png' % game.id)
    if not os.path.exists(filename):
        ImageGenerator.generate(game.text).save(filename)
    with open(filename, 'rb') as f:
        return django.http.HttpResponse(f.read(), content_type='image/png')


@decorators.auth_only
def contest_update(request, game_id):
    game_id = int(game_id)
    game = get_object_or_404(models.ContestGame, id=game_id)

    if request.user not in game.users.all():
        return django.http.HttpResponseBadRequest('Invalid game id')
    if game.state != 'running':
        return django.http.HttpResponseBadRequest('Game has been finished already')

    current_text = request.POST.get('text')
    if current_text is None:
        return django.http.HttpResponseBadRequest()

    last_text = models.LastText(user=request.user, game_type='contest', game_id=game.id, last_text=current_text)
    last_text.save()

    last_texts = models.LastText.objects. \
        filter(game_type='contest', game_id=game.id). \
        values('user__first_name', 'user__last_name', 'last_text')
    competitors = {'%s %s' % (info['user__first_name'], info['user__last_name']):
                        min(100, int(len(info['last_text']) / len(game.text) * 100)) for info in last_texts}

    diff_position = code_database.find_diff_position(game.text, current_text)

    # Decrement because we want to set cursor before error, not after
    if diff_position is not None:
        diff_position -= 1

    diff_position = code_database.get_row_and_column(current_text, diff_position)
    return django.http.JsonResponse({'success': True, 'diff_position': diff_position, 'competitors': competitors})


@decorators.auth_only
def contest_finish(request, game_id):
    game_id = int(game_id)
    game = get_object_or_404(models.ContestGame, id=game_id)

    if request.user not in game.users.all():
        return django.http.HttpResponseBadRequest('Invalid game id')
    if game.state != 'running':
        return django.http.HttpResponseBadRequest('Game has been finished already')

    current_text = request.POST.get('text')
    if current_text is None:
        return django.http.HttpResponseBadRequest()

    last_text = models.LastText(user=request.user, game_type='contest', game_id=game_id, last_text=current_text)
    last_text.save()

    game.finished_users.add(request.user)
    game.save()

    diff_position = code_database.find_diff_position(game.text, current_text)
    distance = code_database.levenshtein_distance(game.text, current_text)

    seconds = int((datetime.now() - game.start_time).total_seconds())
    chars = len(game.text)
    total_seconds = seconds + distance * local_settings.LEVENSHTEIN_PENALTY
    speed = int((chars / total_seconds) * 60)

    score = models.Score(user=request.user,
                         game=game,
                         seconds=seconds,
                         distance=distance,
                         total_seconds=total_seconds,
                         speed=speed)
    score.save()

    return django.http.JsonResponse({'success': True,
                                     'diff_position': diff_position,
                                     'distance': distance,
                                     'speed': speed,
                                     'seconds': seconds,
                                     'total_seconds': '%d + %d x %d = %d' % (
                                         seconds, local_settings.LEVENSHTEIN_PENALTY, distance, total_seconds)})


def scoreboard(request):
    results = models.Score.objects. \
        values('user__first_name', 'user__last_name', 'user__photo_50', 'game__language'). \
        annotate(max_speed=django.db.models.Max('speed')). \
        order_by('-max_speed')
    return render(request, 'scoreboard.html', {'results': results, 'languages': code_database.LANGUAGES})


@decorators.manage_only
def manage(request):
    return render(request, 'manage.html')


@decorators.manage_only
def manage_create(request):
    language = request.GET.get('language')
    if language is None:
        return django.http.HttpResponseBadRequest('language isn\'t defined')
    if language not in code_database.LANGUAGES.keys():
        return django.http.HttpResponseBadRequest('Bad language')

    text = code_database.get_code(language, 'contest')
    game = models.ContestGame(language=language, text=text, password=generate_password(), state='not-started')
    game.save()

    return django.http.HttpResponseRedirect('/manage/contest/%d' % game.id)


@decorators.manage_only
def manage_contest(request, game_id):
    game_id = int(game_id)
    game = get_object_or_404(models.ContestGame, id=game_id)

    return render(request, 'manage_contest.html', {'game': game})


@decorators.manage_only
def manage_start(request, game_id):
    game_id = int(game_id)
    game = get_object_or_404(models.ContestGame, id=game_id)

    game.state = 'running'
    game.start_time = datetime.now() + timedelta(seconds=10)
    game.save()

    return django.http.JsonResponse({'success': True})


@decorators.manage_only
def manage_status(request, game_id):
    game_id = int(game_id)
    game = get_object_or_404(models.ContestGame, id=game_id)

    game_users = game.users.all()
    game_finished_users = game.finished_users.all()
    users = {user.vk_id: {'full_name': user.full_name,
                          'photo_50': user.photo_50,
                          'finished': user in game_finished_users}
             for user in game_users}

    if game.start_time is None:
        seconds_from_start = 0
    else:
        seconds_from_start = (datetime.now() - game.start_time).total_seconds()

    last_texts_db = models.LastText.objects.filter(game_type='contest', game_id=game_id)
    last_texts = {}
    for last_text in last_texts_db:
        last_texts[last_text.user.vk_id] = {'text': last_text.last_text,
                                            'speed': int(len(last_text.last_text) / seconds_from_start * 60)}

    scores = list(models.Score.objects.filter(game_id=game.id).values('user_id', 'seconds', 'distance', 'total_seconds',
                                                                      'speed').all())
    scores = {score['user_id']: score for score in scores}

    return django.http.JsonResponse({'state': game.state,
                                     'users': users,
                                     'last_texts': last_texts,
                                     'password': game.password,
                                     'scores': scores})