# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('folders', '0010_auto_20150902_1220'),
    ]

    operations = [
        migrations.AlterField(
            model_name='folder',
            name='created_on',
            field=models.DateTimeField(blank=True, verbose_name='Дата створення', null=True),
        ),
    ]
