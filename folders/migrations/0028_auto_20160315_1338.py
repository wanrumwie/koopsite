# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('folders', '0027_auto_20160121_0907'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='report',
            options={'permissions': (('view_report', 'Can view report'), ('download_report', 'Can download report')), 'verbose_name': 'файл', 'verbose_name_plural': 'файли'},
        ),
    ]
