# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('flats', '0006_auto_20150801_1317'),
        ('koopsite', '0003_auto_20150831_1716'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='flat',
            field=models.ForeignKey(related_name='userprofiles', blank=True, null=True, to='flats.Flat', verbose_name='Квартира:'),
        ),
    ]
