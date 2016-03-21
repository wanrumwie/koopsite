# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import folders.models


class Migration(migrations.Migration):

    dependencies = [
        ('folders', '0023_auto_20151223_1421'),
    ]

    operations = [
        migrations.AlterField(
            model_name='report',
            name='file',
            field=models.FileField(upload_to=folders.models.Report.get_file_path, default=None, verbose_name='Файл'),
        ),
        migrations.AlterField(
            model_name='report',
            name='filename',
            field=models.CharField(max_length=512, blank=True, verbose_name='Назва файлу'),
        ),
    ]
