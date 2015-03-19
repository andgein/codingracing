__author__ = 'Andrew Gein <andgein@yandex.ru>'

import hashlib

import django.http

import CodingRacing.models as models
import CodingRacing.local_settings as local_settings


def get_auth_cookie(user_id):
    data = str(user_id) + local_settings.COOKIE_HASH
    return hashlib.md5(data.encode()).hexdigest()


def get_user_by_request(request):
    if 'vk_id' not in request.COOKIES or 'auth' not in request.COOKIES:
        return False
    try:
        vk_id = int(request.COOKIES['vk_id'])
    except ValueError:
        return False

    auth_cookie = request.COOKIES['auth']
    if auth_cookie != get_auth_cookie(vk_id):
        return False

    try:
        user = models.User.objects.get(vk_id=vk_id)
        return user
    except models.User.DoesNotExist:
        return False


def auth_only(function):
    def wrap(request, *args, **kwargs):
        user = get_user_by_request(request)
        if not user:
            return django.http.HttpResponseRedirect('/')
        request.user = user
        return function(request, *args, **kwargs)

    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap


def manage_only(function):
    def wrap(request, *args, **kwargs):
        user = get_user_by_request(request)
        if not user:
            return django.http.HttpResponseRedirect('/')
        if user.vk_id not in local_settings.MANAGERS:
            return django.http.HttpResponseRedirect('/')
        request.user = user
        return function(request, *args, **kwargs)

    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap