# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('CodingRacing', '0014_auto_20150320_0448'),
    ]

    operations = [
        migrations.AlterField(
            model_name='score',
            name='game',
            field=models.ForeignKey(help_text='Соревнование', to='CodingRacing.TrainingGame'),
            preserve_default=True,
        ),
    ]
