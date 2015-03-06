# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('CodingRacing', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='traininggame',
            name='language',
            field=models.CharField(max_length=20, help_text='Язык программирования', choices=[('javascript', 'Javascript'), ('csharp', 'C#')]),
            preserve_default=True,
        ),
    ]
