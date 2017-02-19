# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-19 11:42
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sharesWebApp', '0012_transaction'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='currencyValueBuy',
            field=models.DecimalField(decimal_places=4, default=1, max_digits=10, verbose_name='Divisa compra'),
        ),
        migrations.AddField(
            model_name='transaction',
            name='currencyValueSell',
            field=models.DecimalField(blank=True, decimal_places=4, default=1, max_digits=10, null=True, verbose_name='Divisa venta'),
        ),
        migrations.AlterField(
            model_name='share',
            name='currency',
            field=models.ForeignKey(db_column='idCurrency', default=1, on_delete=django.db.models.deletion.CASCADE, to='sharesWebApp.Currency', verbose_name='Divisa'),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='broker',
            field=models.ForeignKey(db_column='idBroker', default=1, on_delete=django.db.models.deletion.CASCADE, to='sharesWebApp.Broker', verbose_name='Broker'),
        ),
    ]