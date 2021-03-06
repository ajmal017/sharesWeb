# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-18 18:57
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sharesWebApp', '0009_auto_20170218_1145'),
    ]

    operations = [
        migrations.AddField(
            model_name='currency',
            name='datetime',
            field=models.DateField(blank=True, null=True, verbose_name='Actual.'),
        ),
        migrations.AddField(
            model_name='currency',
            name='euro',
            field=models.DecimalField(blank=True, decimal_places=4, max_digits=10, null=True, verbose_name='Euros'),
        ),
        migrations.AddField(
            model_name='currency',
            name='ticker',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='Ticker'),
        ),
        migrations.AddField(
            model_name='currency',
            name='update',
            field=models.BooleanField(default=True, verbose_name='Actualizar'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='share',
            name='datetime',
            field=models.DateField(blank=True, null=True, verbose_name='Actual.'),
        ),
        migrations.AddField(
            model_name='share',
            name='lastValue',
            field=models.DecimalField(blank=True, decimal_places=4, max_digits=10, null=True, verbose_name='Valor'),
        ),
        migrations.AddField(
            model_name='share',
            name='update',
            field=models.BooleanField(default=True, verbose_name='Actualizar'),
            preserve_default=False,
        ),
    ]
