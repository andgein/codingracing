# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import CodingRacing.models


class Migration(migrations.Migration):

    dependencies = [
        ('CodingRacing', '0013_auto_20150319_1912'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contestgame',
            name='language',
            field=models.CharField(help_text='Язык программирования', max_length=20, choices=[('javascript', 'JavaScript'), ('csharp', 'C#')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='contestgame',
            name='password',
            field=models.CharField(help_text='Пароль для вступления в игру', db_index=True, max_length=10),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='contestgame',
            name='state',
            field=models.CharField(help_text='Состояние игры', max_length=15, choices=[('finished', 'Finished'), ('not-started', 'Not started yet'), ('running', 'Running...')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='lasttext',
            name='game_id',
            field=models.IntegerField(db_index=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='lasttext',
            name='game_type',
            field=models.CharField(db_index=True, max_length=10, choices=[('contest', CodingRacing.models.ContestGame), ('training', CodingRacing.models.TrainingGame)]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='score',
            name='seconds',
            field=models.IntegerField(help_text='Количество секунд, потраченное на набор текста'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='traininggame',
            name='language',
            field=models.CharField(help_text='Язык программирования', max_length=20, choices=[('javascript', 'JavaScript'), ('csharp', 'C#')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='traininggame',
            name='state',
            field=models.CharField(help_text='Состояние игры', max_length=15, choices=[('finished', 'Finished'), ('not-started', 'Not started yet'), ('running', 'Running...')]),
            preserve_default=True,
        ),
    ]
