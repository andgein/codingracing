# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
import CodingRacing.models


class Migration(migrations.Migration):

    dependencies = [
        ('CodingRacing', '0009_auto_20150316_0646'),
    ]

    operations = [
        migrations.AddField(
            model_name='contestgame',
            name='create_time',
            field=models.DateTimeField(help_text='Время создания игры по серверу', default=datetime.datetime.now),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='contestgame',
            name='password',
            field=models.CharField(max_length=10, help_text='Пароль для вступления в игру', default=''),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='contestgame',
            name='start_time',
            field=models.DateTimeField(null=True, help_text='Время начала игры по серверу', default=None),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='contestgame',
            name='state',
            field=models.CharField(max_length=10, help_text='Состояние игры', choices=[('finished', 'Finished'), ('running', 'Running...')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='lasttext',
            name='game_type',
            field=models.CharField(max_length=10, choices=[('contest', CodingRacing.models.ContestGame), ('training', CodingRacing.models.TrainingGame)]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='traininggame',
            name='state',
            field=models.CharField(max_length=10, help_text='Состояние игры', choices=[('finished', 'Finished'), ('running', 'Running...')]),
            preserve_default=True,
        ),
    ]
