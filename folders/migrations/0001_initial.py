# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Folder',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('name', models.CharField(max_length=256, verbose_name='Тека')),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('parent', models.ForeignKey(related_name='children', to='folders.Folder', default=None, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Report',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('filename', models.CharField(max_length=512)),
                ('file', models.FileField(upload_to='uploads', verbose_name='Документ')),
                ('folder', models.ForeignKey(related_name='reports', to='folders.Folder', default=None, null=True)),
            ],
        ),
    ]
