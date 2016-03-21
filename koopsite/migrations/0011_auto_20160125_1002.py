# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('koopsite', '0010_auto_20151223_1421'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='userprofile',
            options={'permissions': (('activate_account', 'Can activate/deactivate account'), ('view_userprofile', 'Can view user profile')), 'verbose_name': 'профіль користувача', 'verbose_name_plural': 'профілі користувачів'},
        ),
    ]
