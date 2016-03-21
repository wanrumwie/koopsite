# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('folders', '0017_auto_20151022_1711'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='folder',
            options={'permissions': (('view_folder', 'Can view folder'), ('download_folder', 'Can download folder'))},
        ),
    ]
