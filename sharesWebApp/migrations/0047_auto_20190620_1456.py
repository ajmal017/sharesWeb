# -*- coding: utf-8 -*-
# Generated by Django 1.11.18 on 2019-06-20 14:56
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sharesWebApp', '0046_transaction_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='dividend',
            name='description',
            field=models.CharField(blank=True, max_length=8000, null=True, verbose_name='Notas'),
        ),
        migrations.AddField(
            model_name='right',
            name='description',
            field=models.CharField(blank=True, max_length=8000, null=True, verbose_name='Notas'),
        ),
    ]