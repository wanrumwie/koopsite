# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('koopsite', '0004_userprofile_flat'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='flat_No',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='website',
        ),
    ]
