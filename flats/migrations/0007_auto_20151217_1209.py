# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('flats', '0006_auto_20150801_1317'),
    ]

    operations = [
        migrations.AlterField(
            model_name='flat',
            name='bathroom_S',
            field=models.FloatField(default=0, verbose_name='ванна'),
        ),
        migrations.AlterField(
            model_name='flat',
            name='bti_plan',
            field=models.FloatField(default=0, verbose_name='БТІ - Типовий'),
        ),
        migrations.AlterField(
            model_name='flat',
            name='corridor_S',
            field=models.FloatField(default=0, verbose_name='коридор'),
        ),
        migrations.AlterField(
            model_name='flat',
            name='deviation',
            field=models.FloatField(default=0, verbose_name='% відхилення'),
        ),
        migrations.AlterField(
            model_name='flat',
            name='entrance_No',
            field=models.IntegerField(default=0, verbose_name="Під'їзд"),
        ),
        migrations.AlterField(
            model_name='flat',
            name='flat_99',
            field=models.IntegerField(default=0, verbose_name='Кв № 99'),
        ),
        migrations.AlterField(
            model_name='flat',
            name='flat_No',
            field=models.CharField(max_length=5, verbose_name='Квартира №'),
        ),
        migrations.AlterField(
            model_name='flat',
            name='floor_No',
            field=models.IntegerField(default=0, verbose_name='Поверх'),
        ),
        migrations.AlterField(
            model_name='flat',
            name='kitchen_S',
            field=models.FloatField(default=0, verbose_name='кухня'),
        ),
        migrations.AlterField(
            model_name='flat',
            name='larder1_S',
            field=models.FloatField(default=0, verbose_name='комора'),
        ),
        migrations.AlterField(
            model_name='flat',
            name='larder2_S',
            field=models.FloatField(default=0, verbose_name='2-га комора'),
        ),
        migrations.AlterField(
            model_name='flat',
            name='listing',
            field=models.IntegerField(default=0, verbose_name='Список'),
        ),
        migrations.AlterField(
            model_name='flat',
            name='loggia_S',
            field=models.FloatField(default=0, verbose_name='лоджія'),
        ),
        migrations.AlterField(
            model_name='flat',
            name='note',
            field=models.CharField(default='', max_length=10, verbose_name='Примітка'),
        ),
        migrations.AlterField(
            model_name='flat',
            name='room1_S',
            field=models.FloatField(default=0, verbose_name='кімната'),
        ),
        migrations.AlterField(
            model_name='flat',
            name='room2_S',
            field=models.FloatField(default=0, verbose_name='2-га кімната'),
        ),
        migrations.AlterField(
            model_name='flat',
            name='room3_S',
            field=models.FloatField(default=0, verbose_name='3-тя кімната'),
        ),
        migrations.AlterField(
            model_name='flat',
            name='rooms',
            field=models.IntegerField(default=0, verbose_name='Кімнат'),
        ),
        migrations.AlterField(
            model_name='flat',
            name='s0_BTI',
            field=models.FloatField(default=0, verbose_name='в тч житлова (БТІ)'),
        ),
        migrations.AlterField(
            model_name='flat',
            name='s0_plan',
            field=models.FloatField(default=0, verbose_name='Типовий поверх Житлова'),
        ),
        migrations.AlterField(
            model_name='flat',
            name='s_BTI',
            field=models.FloatField(default=0, verbose_name='Загальна площа (БТІ)'),
        ),
        migrations.AlterField(
            model_name='flat',
            name='s_plan',
            field=models.FloatField(default=0, verbose_name='Типовий поверх Загальна'),
        ),
        migrations.AlterField(
            model_name='flat',
            name='toilet_S',
            field=models.FloatField(default=0, verbose_name='вбиральня'),
        ),
    ]
