# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import folders.models


class Migration(migrations.Migration):

    dependencies = [
        ('folders', '0003_auto_20150801_2001'),
    ]

    operations = [
        migrations.AlterField(
            model_name='report',
            name='file',
            field=models.FileField(verbose_name='Документ', upload_to=folders.models.Report.get_file_path, null=True, blank=True),
        ),
    ]
