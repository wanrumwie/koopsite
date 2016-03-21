# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('folders', '0014_auto_20150908_1212'),
    ]

    operations = [
        migrations.RenameField(
            model_name='report',
            old_name='folder',
            new_name='parent',
        ),
    ]
