# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('folders', '0006_auto_20150831_1716'),
    ]

    operations = [
        migrations.AddField(
            model_name='report',
            name='filename',
            field=models.CharField(verbose_name='Назва файлу', null=True, blank=True, max_length=512),
        ),
    ]
