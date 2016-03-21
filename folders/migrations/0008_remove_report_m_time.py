# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('folders', '0007_report_filename'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='report',
            name='m_time',
        ),
    ]
