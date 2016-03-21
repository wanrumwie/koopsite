# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('flats', '0007_auto_20151217_1209'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='flat',
            options={'verbose_name_plural': 'квартири', 'verbose_name': 'квартира'},
        ),
        migrations.AlterModelOptions(
            name='person',
            options={'verbose_name_plural': 'особи', 'verbose_name': 'особа'},
        ),
    ]
