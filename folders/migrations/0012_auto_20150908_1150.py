# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('folders', '0011_auto_20150902_1229'),
    ]

    operations = [
        migrations.AlterField(
            model_name='folder',
            name='name',
            field=models.CharField(verbose_name='Тека', max_length=256, unique=True, error_messages={'unique': 'Така назва вже існує!'}),
        ),
    ]
