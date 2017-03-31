# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import CodingRacing.models


class Migration(migrations.Migration):

    dependencies = [
        ('CodingRacing', '0016_auto_20150424_0035'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contestgame',
            name='language',
            field=models.CharField(max_length=20, choices=[('csharp', 'C#'), ('python', 'Python'), ('asm', 'ASM'), ('javascript', 'JavaScript')], help_text='Язык программирования'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='contestgame',
            name='state',
            field=models.CharField(max_length=15, choices=[('running', 'Running...'), ('not-started', 'Not started yet'), ('finished', 'Finished')], help_text='Состояние игры'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='lasttext',
            name='game_type',
            field=models.CharField(max_length=10, choices=[('training', CodingRacing.models.TrainingGame), ('contest', CodingRacing.models.ContestGame)], db_index=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='traininggame',
            name='language',
            field=models.CharField(max_length=20, choices=[('csharp', 'C#'), ('python', 'Python'), ('asm', 'ASM'), ('javascript', 'JavaScript')], help_text='Язык программирования'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='traininggame',
            name='state',
            field=models.CharField(max_length=15, choices=[('running', 'Running...'), ('not-started', 'Not started yet'), ('finished', 'Finished')], help_text='Состояние игры'),
            preserve_default=True,
        ),
    ]
