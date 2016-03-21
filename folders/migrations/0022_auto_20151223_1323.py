# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('folders', '0021_auto_20151221_1329'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='folder',
            options={'permissions': (('view_folder', 'Can view folder'), ('download_folder', 'Can download folder')), 'verbose_name_plural': 'теки', 'verbose_name': 'тека'},
        ),
    ]
