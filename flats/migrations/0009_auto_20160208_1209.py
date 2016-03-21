# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('flats', '0008_auto_20151223_1421'),
    ]

    operations = [
        migrations.AlterField(
            model_name='flat',
            name='entrance_No',
            field=models.CharField(max_length=5, verbose_name="Під'їзд"),
        ),
        migrations.AlterField(
            model_name='flat',
            name='floor_No',
            field=models.CharField(max_length=5, verbose_name='Поверх'),
        ),
    ]
