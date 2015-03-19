# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import CodingRacing.models


class Migration(migrations.Migration):

    dependencies = [
        ('CodingRacing', '0011_auto_20150316_0801'),
    ]

    operations = [
        migrations.AddField(
            model_name='contestgame',
            name='finished_users',
            field=models.ManyToManyField(to='CodingRacing.User', null=True, related_name='finished_in_contests'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='contestgame',
            name='language',
            field=models.CharField(help_text='Язык программирования', max_length=20, choices=[('csharp', 'C#'), ('javascript', 'Javascript')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='lasttext',
            name='game_type',
            field=models.CharField(choices=[('contest', CodingRacing.models.ContestGame), ('training', CodingRacing.models.TrainingGame)], max_length=10),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='traininggame',
            name='language',
            field=models.CharField(help_text='Язык программирования', max_length=20, choices=[('csharp', 'C#'), ('javascript', 'Javascript')]),
            preserve_default=True,
        ),
    ]
