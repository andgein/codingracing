# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('CodingRacing', '0002_auto_20150306_1850'),
    ]

    operations = [
        migrations.AlterField(
            model_name='traininggame',
            name='start_time',
            field=models.DateTimeField(help_text='Время начала игры по серверу', default=django.utils.timezone.now),
            preserve_default=True,
        ),
    ]
