# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('folders', '0022_auto_20151223_1323'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='report',
            options={'verbose_name_plural': 'документи', 'permissions': (('view_report', 'Can view report'), ('download_report', 'Can download report')), 'verbose_name': 'документ'},
        ),
    ]
