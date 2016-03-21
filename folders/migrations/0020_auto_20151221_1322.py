# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('folders', '0019_auto_20151028_1426'),
    ]

    operations = [
        migrations.AlterField(
            model_name='folder',
            name='created_on',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Дата створення', null=True),
        ),
    ]
