# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-12 18:03
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sharesWebApp', '0031_auto_20170312_1719'),
    ]

    operations = [
        migrations.CreateModel(
            name='BrokerComissions',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(verbose_name='Fecha')),
                ('amount', models.DecimalField(decimal_places=4, max_digits=10, verbose_name='Importe')),
                ('description', models.CharField(blank=True, max_length=8000, null=True, verbose_name='Notas')),
                ('broker', models.ForeignKey(db_column='idBroker', default=1, on_delete=django.db.models.deletion.CASCADE, to='sharesWebApp.Broker', verbose_name='Broker')),
            ],
            options={
                'ordering': ['date'],
                'db_table': 'BrokerComissions',
                'verbose_name': 'Comisiones globales',
                'verbose_name_plural': 'Comisiones globales',
            },
        ),
        migrations.AlterModelOptions(
            name='depositwithdraw',
            options={'ordering': ['date'], 'verbose_name': 'Depositos/Reembolsos', 'verbose_name_plural': 'Depositos/Reembolsos'},
        ),
    ]