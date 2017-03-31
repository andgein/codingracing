from django.db import models
from django.contrib import admin
from datetime import datetime

from CodingRacing import code_database


class User(models.Model):
    vk_id = models.IntegerField(primary_key=True)
    create_time = models.DateTimeField(auto_now_add=True, help_text='Время создания пользователя')
    modify_time = models.DateTimeField(auto_now=True, help_text='Время изменения пользователя')

    first_name = models.CharField(max_length=100, help_text='Имя')
    last_name = models.CharField(max_length=100, help_text='Фамилия')
    photo_50 = models.CharField(max_length=100, help_text='URL аватарки')
    city = models.CharField(max_length=100, help_text='Город')

    def __str__(self):
        return '%s %s' % (self.first_name, self.last_name)

    @property
    def full_name(self):
        return '%s %s' % (self.first_name, self.last_name)


GAME_STATES = {'not-started': 'Not started yet', 'running': 'Running...', 'finished': 'Finished'}


class Game(models.Model):
    language = models.CharField(max_length=20, choices=code_database.LANGUAGES.items(),
                                help_text='Язык программирования')
    text = models.TextField(help_text='Текст программы')
    state = models.CharField(max_length=15, choices=GAME_STATES.items(), help_text='Состояние игры')

    class Meta:
        abstract = True


class TrainingGame(Game):
    user = models.ForeignKey(User, help_text='Пользователь')

    start_time = models.DateTimeField(default=datetime.now, help_text='Время начала игры по серверу')
    start_client_time = models.DateTimeField(help_text='Время начала игры по клиенту')
    finish_time = models.DateTimeField(default=None, null=True, help_text='Время окончания игры по серверу')
    finish_client_time = models.DateTimeField(default=None, null=True, help_text='Время окончания игры по клиенту')

    def __str__(self):
        return 'Game at %s, %s [%s]' % (self.start_time, self.language, self.state)


class ContestGame(Game):
    users = models.ManyToManyField(User, null=True)
    finished_users = models.ManyToManyField(User, null=True, related_name='finished_in_contests')

    password = models.CharField(max_length=10, db_index=True, help_text='Пароль для вступления в игру')

    create_time = models.DateTimeField(default=datetime.now, help_text='Время создания игры по серверу')
    start_time = models.DateTimeField(default=None, null=True, help_text='Время начала игры по серверу')


class LastText(models.Model):
    user = models.ForeignKey(User, db_index=True, help_text='Пользователь')
    last_text = models.TextField(default='', help_text='Последний присланный текст от клиента')

    time = models.DateTimeField(default=datetime.now, help_text='Время')
    game_type = models.CharField(max_length=10, db_index=True,
                                 choices={'training': TrainingGame, 'contest': ContestGame}.items())
    game_id = models.IntegerField(db_index=True)

    def __str__(self):
        return '%s-%d, %s, by %s, "%s"' % (
            self.game_type, self.game_id, self.time, self.user.first_name + ' ' + self.user.last_name,
            self.last_text[:30])


class Score(models.Model):
    user = models.ForeignKey(User, db_index=True, help_text='Пользователь')
    game = models.ForeignKey(ContestGame, db_index=True, help_text='Соревнование')

    seconds = models.IntegerField(help_text='Количество секунд, потраченное на набор текста')
    distance = models.IntegerField(help_text='Расстояние Левенштейна')
    total_seconds = models.IntegerField(help_text='Суммарное время, вместе со штрафом')
    speed = models.IntegerField(help_text='Скорость')

    time = models.DateTimeField(default=datetime.now, help_text='Время установки результата')


admin.site.register(User)
admin.site.register(TrainingGame)
admin.site.register(ContestGame)
admin.site.register(LastText)
admin.site.register(Score)
