# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('folders', '0020_auto_20151221_1322'),
    ]

    operations = [
        migrations.AlterField(
            model_name='folder',
            name='created_on',
            field=models.DateTimeField(null=True, blank=True, verbose_name='Дата створення'),
        ),
    ]
