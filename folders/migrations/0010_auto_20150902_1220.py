# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('folders', '0009_auto_20150902_1155'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='folder',
            name='uploaded_on',
        ),
        migrations.AddField(
            model_name='folder',
            name='created_on',
            field=models.DateTimeField(null=True, auto_now_add=True, verbose_name='Дата створення'),
        ),
    ]
