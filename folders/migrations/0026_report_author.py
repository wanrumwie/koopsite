# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('folders', '0025_auto_20160110_1436'),
    ]

    operations = [
        migrations.AddField(
            model_name='report',
            name='author',
            field=models.ForeignKey(blank=True, null=True, related_name='reports', verbose_name='Автор', to=settings.AUTH_USER_MODEL),
        ),
    ]
