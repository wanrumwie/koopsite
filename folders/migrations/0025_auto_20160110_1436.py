# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('folders', '0024_auto_20160110_1309'),
    ]

    operations = [
        migrations.AlterField(
            model_name='report',
            name='filename',
            field=models.CharField(max_length=512, null=True, verbose_name='Назва файлу'),
        ),
    ]
