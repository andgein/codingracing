# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('CodingRacing', '0004_auto_20150306_2325'),
    ]

    operations = [
        migrations.AddField(
            model_name='traininggame',
            name='state',
            field=models.CharField(help_text='Состояние игры', default='finished', choices=[('running', 'Running...'), ('finished', 'Finished')], max_length=10),
            preserve_default=False,
        ),
    ]
