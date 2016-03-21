# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('folders', '0008_remove_report_m_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='folder',
            name='uploaded_on',
            field=models.DateTimeField(null=True, verbose_name='Дата заладування', auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='report',
            name='uploaded_on',
            field=models.DateTimeField(null=True, verbose_name='Дата заладування', auto_now_add=True),
        ),
    ]
