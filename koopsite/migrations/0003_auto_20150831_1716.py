# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import koopsite.models


class Migration(migrations.Migration):

    dependencies = [
        ('koopsite', '0002_auto_20150803_1838'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='flat_No',
            field=models.CharField(verbose_name='Квартира №:', blank=True, max_length=5),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='picture',
            field=models.ImageField(help_text='Виберіть зображення, яке слід вивантажити у Ваш профіль.', blank=True, verbose_name='Ваше фото:', upload_to=koopsite.models.UserProfile.get_file_path),
        ),
    ]
