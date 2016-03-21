# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('folders', '0013_auto_20150908_1208'),
    ]

    operations = [
        migrations.AlterField(
            model_name='folder',
            name='name',
            field=models.CharField(error_messages={'unique': 'Така назва вже існує!'}, verbose_name='Тека', max_length=256),
        ),
    ]
