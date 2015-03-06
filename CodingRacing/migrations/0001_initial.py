# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='TrainingGame',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('start_time', models.DateTimeField(default=datetime.datetime.now, help_text='Время начала игры по серверу')),
                ('start_client_time', models.DateTimeField(help_text='Время начала игры по клиенту')),
                ('language', models.CharField(max_length=20, choices=[('csharp', 'C#'), ('javascript', 'Javascript')], help_text='Язык программирования')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('vk_id', models.IntegerField(primary_key=True, serialize=False)),
                ('create_time', models.DateTimeField(auto_now_add=True, help_text='Время создания пользователя')),
                ('modify_time', models.DateTimeField(auto_now=True, help_text='Время изменения пользователя')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='traininggame',
            name='user',
            field=models.ForeignKey(to='CodingRacing.User', help_text='Пользователь'),
            preserve_default=True,
        ),
    ]
