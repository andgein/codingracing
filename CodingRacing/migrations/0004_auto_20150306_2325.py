# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('CodingRacing', '0003_auto_20150306_1853'),
    ]

    operations = [
        migrations.AddField(
            model_name='traininggame',
            name='last_text',
            field=models.TextField(help_text='Последний присланный текст от клиента', default=''),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='traininggame',
            name='start_time',
            field=models.DateTimeField(help_text='Время начала игры по серверу', default=datetime.datetime.now),
            preserve_default=True,
        ),
    ]
