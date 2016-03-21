# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('folders', '0002_auto_20150801_1954'),
    ]

    operations = [
        migrations.AlterField(
            model_name='folder',
            name='created_on',
            field=models.DateTimeField(null=True, auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='folder',
            name='parent',
            field=models.ForeignKey(to='folders.Folder', null=True, related_name='children', blank=True, default=None),
        ),
        migrations.AlterField(
            model_name='report',
            name='file',
            field=models.FileField(null=True, upload_to='uploads', verbose_name='Документ', blank=True),
        ),
        migrations.AlterField(
            model_name='report',
            name='folder',
            field=models.ForeignKey(to='folders.Folder', null=True, related_name='reports', blank=True, default=None),
        ),
    ]
