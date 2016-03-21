# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('flats', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='person',
            name='flat',
            field=models.ForeignKey(default=0, to='flats.Flat'),
            preserve_default=False,
        ),
    ]
