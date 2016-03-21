# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('flats', '0003_auto_20150717_1632'),
    ]

    operations = [
        migrations.AlterField(
            model_name='flat',
            name='note',
            field=models.CharField(max_length=10, default=''),
        ),
    ]
