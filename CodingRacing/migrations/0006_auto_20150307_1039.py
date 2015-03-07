# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('CodingRacing', '0005_traininggame_state'),
    ]

    operations = [
        migrations.AddField(
            model_name='traininggame',
            name='finish_client_time',
            field=models.DateTimeField(null=True, default=None, help_text='Время окончания игры по клиенту'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='traininggame',
            name='finish_time',
            field=models.DateTimeField(null=True, default=None, help_text='Время окончания игры по серверу'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='traininggame',
            name='language',
            field=models.CharField(max_length=20, help_text='Язык программирования', choices=[('csharp', 'C#'), ('javascript', 'Javascript')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='traininggame',
            name='state',
            field=models.CharField(max_length=10, help_text='Состояние игры', choices=[('finished', 'Finished'), ('running', 'Running...')]),
            preserve_default=True,
        ),
    ]
