# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import folders.models


class Migration(migrations.Migration):

    dependencies = [
        ('folders', '0016_auto_20151020_2223'),
    ]

    operations = [
        migrations.AlterField(
            model_name='report',
            name='file',
            field=models.FileField(upload_to=folders.models.Report.get_file_path, verbose_name='Файл', null=True, blank=True),
        ),
    ]
