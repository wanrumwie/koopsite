# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('folders', '0005_auto_20150803_1838'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='folder',
            name='created_on',
        ),
        migrations.RemoveField(
            model_name='report',
            name='filename',
        ),
        migrations.AddField(
            model_name='report',
            name='m_time',
            field=models.DateTimeField(verbose_name='Дата змінення', blank=True, null=True),
        ),
        migrations.AddField(
            model_name='report',
            name='uploaded_on',
            field=models.DateTimeField(verbose_name='Дата вивантаження', auto_now_add=True, null=True),
        ),
        migrations.AlterField(
            model_name='folder',
            name='parent',
            field=models.ForeignKey(to='folders.Folder', blank=True, default=None, verbose_name='Материнська тека', related_name='children', null=True),
        ),
        migrations.AlterField(
            model_name='report',
            name='folder',
            field=models.ForeignKey(to='folders.Folder', default=None, verbose_name='Тека', related_name='reports'),
        ),
    ]
