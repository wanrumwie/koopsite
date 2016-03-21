# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('folders', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='folder',
            name='parent',
            field=models.ForeignKey(blank=True, to='folders.Folder', related_name='children', default=None),
        ),
        migrations.AlterField(
            model_name='report',
            name='file',
            field=models.FileField(verbose_name='Документ', upload_to='uploads', blank=True),
        ),
        migrations.AlterField(
            model_name='report',
            name='folder',
            field=models.ForeignKey(blank=True, to='folders.Folder', related_name='reports', default=None),
        ),
    ]
