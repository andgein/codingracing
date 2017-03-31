# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('CodingRacing', '0015_auto_20150327_0428'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contestgame',
            name='state',
            field=models.CharField(help_text='Состояние игры', max_length=15, choices=[('running', 'Running...'), ('finished', 'Finished'), ('not-started', 'Not started yet')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='score',
            name='game',
            field=models.ForeignKey(help_text='Соревнование', to='CodingRacing.ContestGame'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='traininggame',
            name='state',
            field=models.CharField(help_text='Состояние игры', max_length=15, choices=[('running', 'Running...'), ('finished', 'Finished'), ('not-started', 'Not started yet')]),
            preserve_default=True,
        ),
    ]
