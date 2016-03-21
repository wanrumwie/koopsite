# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import koopsite.models


class Migration(migrations.Migration):

    dependencies = [
        ('koopsite', '0006_auto_20151108_1003'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='is_recognized',
            field=models.NullBooleanField(default=None, verbose_name='Підтверджений'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='picture',
            field=models.ImageField(blank=True, upload_to=koopsite.models.UserProfile.get_file_path, verbose_name='Аватар'),
        ),
    ]
