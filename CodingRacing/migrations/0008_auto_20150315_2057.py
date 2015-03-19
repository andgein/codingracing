# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('CodingRacing', '0007_traininggame_text'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='city',
            field=models.CharField(max_length=100, help_text='Город', default=''),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='user',
            name='first_name',
            field=models.CharField(max_length=100, help_text='Имя', default=''),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='user',
            name='last_name',
            field=models.CharField(max_length=100, help_text='Фамилия', default=''),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='user',
            name='photo_50',
            field=models.CharField(max_length=100, help_text='URL аватарки', default=''),
            preserve_default=False,
        ),
    ]
