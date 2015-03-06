__author__ = 'Andrew Gein <andgein@yandex.ru>'

from django.db import models

from datetime import datetime


class User(models.Model):
    vk_id = models.IntegerField(primary_key=True)
    create_time = models.DateTimeField(auto_now_add=True, help_text='Время создания пользователя')
    modify_time = models.DateTimeField(auto_now=True, help_text='Время изменения пользователя')


LANGUAGES = {'csharp': 'C#', 'javascript': 'Javascript'}


class TrainingGame(models.Model):
    user = models.ForeignKey(User, help_text='Пользователь')

    start_time = models.DateTimeField(default=datetime.now, help_text='Время начала игры по серверу')
    start_client_time = models.DateTimeField(help_text='Время начала игры по клиенту')

    language = models.CharField(max_length=20, choices=LANGUAGES.items(), help_text='Язык программирования')
    last_text = models.TextField(default='', help_text='Последний присланный текст от клиента')
