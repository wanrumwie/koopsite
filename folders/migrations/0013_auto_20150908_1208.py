# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('folders', '0012_auto_20150908_1150'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='folder',
            unique_together=set([('parent', 'name')]),
        ),
    ]
