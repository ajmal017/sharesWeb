# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-04-30 19:34
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sharesWebApp', '0041_auto_20170430_1618'),
    ]

    operations = [
        migrations.AddField(
            model_name='share',
            name='targetValue',
            field=models.DecimalField(blank=True, decimal_places=4, max_digits=10, null=True, verbose_name='Objetivo'),
        ),
    ]
