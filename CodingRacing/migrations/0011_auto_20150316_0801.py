# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import CodingRacing.models


class Migration(migrations.Migration):

    dependencies = [
        ('CodingRacing', '0010_auto_20150316_0657'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contestgame',
            name='state',
            field=models.CharField(choices=[('running', 'Running...'), ('finished', 'Finished'), ('not-started', 'Not started yet')], help_text='Состояние игры', max_length=15),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='contestgame',
            name='users',
            field=models.ManyToManyField(null=True, to='CodingRacing.User'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='lasttext',
            name='game_type',
            field=models.CharField(choices=[('training', CodingRacing.models.TrainingGame), ('contest', CodingRacing.models.ContestGame)], max_length=10),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='traininggame',
            name='state',
            field=models.CharField(choices=[('running', 'Running...'), ('finished', 'Finished'), ('not-started', 'Not started yet')], help_text='Состояние игры', max_length=15),
            preserve_default=True,
        ),
    ]
