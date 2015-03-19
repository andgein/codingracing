# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('CodingRacing', '0012_auto_20150316_1041'),
    ]

    operations = [
        migrations.CreateModel(
            name='Score',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('seconds', models.IntegerField(help_text='Количество секунд, потраченное на рабор текста')),
                ('distance', models.IntegerField(help_text='Расстояние Левенштейна')),
                ('total_seconds', models.IntegerField(help_text='Суммарное время, вместе со штрафом')),
                ('speed', models.IntegerField(help_text='Скорость')),
                ('time', models.DateTimeField(help_text='Время установки результата', default=datetime.datetime.now)),
                ('game', models.ForeignKey(help_text='Соревнование', to='CodingRacing.ContestGame')),
                ('user', models.ForeignKey(help_text='Пользователь', to='CodingRacing.User')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterField(
            model_name='contestgame',
            name='state',
            field=models.CharField(help_text='Состояние игры', choices=[('running', 'Running...'), ('not-started', 'Not started yet'), ('finished', 'Finished')], max_length=15),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='traininggame',
            name='state',
            field=models.CharField(help_text='Состояние игры', choices=[('running', 'Running...'), ('not-started', 'Not started yet'), ('finished', 'Finished')], max_length=15),
            preserve_default=True,
        ),
    ]
