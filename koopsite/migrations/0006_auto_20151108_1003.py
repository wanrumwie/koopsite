# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import koopsite.models


class Migration(migrations.Migration):

    dependencies = [
        ('koopsite', '0005_auto_20151022_1734'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='is_recognized',
            field=models.NullBooleanField(help_text='Чи визнаємо за користувачем право на авторизацію.', verbose_name='Підтверджений'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='flat',
            field=models.ForeignKey(null=True, blank=True, related_name='userprofiles', to='flats.Flat', verbose_name='Квартира'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='picture',
            field=models.ImageField(blank=True, help_text='Зображення, яке слід вивантажити у профіль.', upload_to=koopsite.models.UserProfile.get_file_path, verbose_name='Аватар'),
        ),
    ]
