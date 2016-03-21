# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('koopsite', '0009_auto_20151125_1005'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='userprofile',
            options={'verbose_name_plural': 'профілі користувачів', 'permissions': (('activate_account', 'Can activate/deactivate account'),), 'verbose_name': 'профіль користувача'},
        ),
    ]
