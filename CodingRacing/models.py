__author__ = 'Andrew Gein <andgein@yandex.ru>'

from django.db import models
from datetime import datetime

from CodingRacing import code_database


class User(models.Model):
    vk_id = models.IntegerField(primary_key=True)
    create_time = models.DateTimeField(auto_now_add=True, help_text='Время создания пользователя')
    modify_time = models.DateTimeField(auto_now=True, help_text='Время изменения пользователя')


GAME_STATES = {'running': 'Running...', 'finished': 'Finished'}


class TrainingGame(models.Model):
    user = models.ForeignKey(User, help_text='Пользователь')

    start_time = models.DateTimeField(default=datetime.now, help_text='Время начала игры по серверу')
    start_client_time = models.DateTimeField(help_text='Время начала игры по клиенту')
    finish_time = models.DateTimeField(default=None, null=True, help_text='Время окончания игры по серверу')
    finish_client_time = models.DateTimeField(default=None, null=True, help_text='Время окончания игры по клиенту')

    language = models.CharField(max_length=20, choices=code_database.LANGUAGES.items(),
                                help_text='Язык программирования')
    text = models.TextField(help_text='Текст программы')
    last_text = models.TextField(default='', help_text='Последний присланный текст от клиента')
    state = models.CharField(max_length=10, choices=GAME_STATES.items(), help_text='Состояние игры')
