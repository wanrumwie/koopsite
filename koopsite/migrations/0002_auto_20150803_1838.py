# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import koopsite.models


class Migration(migrations.Migration):

    dependencies = [
        ('koopsite', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='picture',
            field=models.ImageField(upload_to=koopsite.models.UserProfile.get_file_path, blank=True),
        ),
    ]
