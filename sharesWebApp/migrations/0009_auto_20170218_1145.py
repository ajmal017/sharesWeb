# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-18 11:45
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sharesWebApp', '0008_auto_20170216_0902'),
    ]

    operations = [
        migrations.CreateModel(
            name='Broker',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Nombre')),
            ],
            options={
                'ordering': ['name'],
                'db_table': 'Broker',
                'verbose_name': 'Broker',
                'verbose_name_plural': 'Brokers',
            },
        ),
        migrations.AlterModelOptions(
            name='sharefonds',
            options={'verbose_name': 'Acciones del Fondo', 'verbose_name_plural': 'Acciones de los Fondos'},
        ),
    ]
