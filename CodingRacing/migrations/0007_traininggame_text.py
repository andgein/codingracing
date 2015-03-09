# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('CodingRacing', '0006_auto_20150307_1039'),
    ]

    operations = [
        migrations.AddField(
            model_name='traininggame',
            name='text',
            field=models.TextField(default='', help_text='Текст программы'),
            preserve_default=False,
        ),
    ]
