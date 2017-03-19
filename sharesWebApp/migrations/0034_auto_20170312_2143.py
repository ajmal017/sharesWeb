# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-12 21:43
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sharesWebApp', '0033_auto_20170312_1901'),
    ]

    operations = [
        migrations.CreateModel(
            name='CurrencyHistory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(verbose_name='Fecha')),
                ('close', models.DecimalField(blank=True, decimal_places=4, max_digits=10, null=True, verbose_name='Cierre')),
                ('change', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True, verbose_name='Cambio (%)')),
                ('currency', models.ForeignKey(db_column='idCurrency', on_delete=django.db.models.deletion.CASCADE, to='sharesWebApp.Currency', verbose_name='Divisa')),
            ],
            options={
                'ordering': ['-date', 'currency'],
                'db_table': 'CurrencyHistory',
                'verbose_name': 'Hist\xf3rico Divisas',
                'verbose_name_plural': 'Hist\xf3rico Divisas',
            },
        ),
        migrations.AlterModelOptions(
            name='sharehistory',
            options={'ordering': ['-date', 'share'], 'verbose_name': 'Hist\xf3rico Acciones', 'verbose_name_plural': 'Hist\xf3rico Acciones'},
        ),
    ]