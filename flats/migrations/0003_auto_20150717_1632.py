# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('flats', '0002_person_flat'),
    ]

    operations = [
        migrations.AlterField(
            model_name='flat',
            name='listing',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='flat',
            name='note',
            field=models.CharField(default=0, max_length=10),
        ),
    ]
