# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
import CodingRacing.models


class Migration(migrations.Migration):

    dependencies = [
        ('CodingRacing', '0008_auto_20150315_2057'),
    ]

    operations = [
        migrations.CreateModel(
            name='ContestGame',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('language', models.CharField(choices=[('javascript', 'Javascript'), ('csharp', 'C#')], max_length=20, help_text='Язык программирования')),
                ('text', models.TextField(help_text='Текст программы')),
                ('state', models.CharField(choices=[('running', 'Running...'), ('finished', 'Finished')], max_length=10, help_text='Состояние игры')),
                ('users', models.ManyToManyField(to='CodingRacing.User')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='LastText',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('last_text', models.TextField(default='', help_text='Последний присланный текст от клиента')),
                ('time', models.DateTimeField(default=datetime.datetime.now, help_text='Время')),
                ('game_type', models.CharField(choices=[('training', CodingRacing.models.TrainingGame), ('contest', CodingRacing.models.ContestGame)], max_length=10)),
                ('game_id', models.IntegerField()),
                ('user', models.ForeignKey(to='CodingRacing.User', help_text='Пользователь')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='traininggame',
            name='last_text',
        ),
        migrations.AlterField(
            model_name='traininggame',
            name='language',
            field=models.CharField(choices=[('javascript', 'Javascript'), ('csharp', 'C#')], max_length=20, help_text='Язык программирования'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='traininggame',
            name='state',
            field=models.CharField(choices=[('running', 'Running...'), ('finished', 'Finished')], max_length=10, help_text='Состояние игры'),
            preserve_default=True,
        ),
    ]
