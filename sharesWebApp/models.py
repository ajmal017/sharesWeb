#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.db import models

class Currency(models.Model):
    name = models.CharField(max_length=255, blank=False, null=False, verbose_name='Nombre')
    symbol = models.CharField(max_length=10, blank=False, null=False, default='', verbose_name='Símbolo')

    class Meta:
        db_table = "Currency"
        ordering = ["name"]
        verbose_name = "Divisa"
        verbose_name_plural = "Divisas"

    def __unicode__(self):
        return self.name


class Index(models.Model):
    name = models.CharField(max_length=255, blank=False, null=False, verbose_name='Nombre')

    class Meta:
        db_table = "Index"
        ordering = ["name"]
        verbose_name = "Mercado"
        verbose_name_plural = "Mercados"

    def __unicode__(self):
        return self.name


class Period(models.Model):
    fromDate = models.DateField(blank=False, null=False, verbose_name='Desde')
    toDate = models.DateField(blank=False, null=False, verbose_name='Hasta')

    class Meta:
        db_table = "Period"
        ordering = ["fromDate"]
        verbose_name = "Periodo"
        verbose_name_plural = "Periodos"

    def __unicode__(self):
        return '{:%d/%m/%Y}'.format(self.fromDate) + ' - ' + '{:%d/%m/%Y}'.format(self.toDate)


class Fond(models.Model):
    name = models.CharField(max_length=255, blank=False, null=False, verbose_name='Nombre')
    iberian = models.BooleanField(blank=False, null=False, verbose_name='Ibérico')

    class Meta:
        db_table = "Fond"
        ordering = ["name"]
        verbose_name = "Fondo"
        verbose_name_plural = "Fondos"

    def __unicode__(self):
        return self.name


class Share(models.Model):
    name = models.CharField(max_length=255, blank=False, null=False, verbose_name='Nombre')
    ISIN = models.CharField(max_length=20, blank=True, null=True)
    currency = models.ForeignKey(Currency, db_column='idCurrency', verbose_name='Divisa')
    index = models.ForeignKey(Index, db_column='idIndex', blank=True, null=True, verbose_name='Mercado')
    ticker = models.CharField(max_length=20, blank=True, null=True, verbose_name='Ticker')
    favourite = models.BooleanField(blank=False, null=False, verbose_name='Favorito')
    description  =  models.CharField(max_length=8000, blank=True, null=True, verbose_name='Descripción')
    fonds = models.ManyToManyField(Fond, through='ShareFonds', through_fields=('share', 'fond'))

    class Meta:
        db_table = "Share"
        ordering = ["name"]
        verbose_name = "Accion"
        verbose_name_plural = "Acciones"

    def __unicode__(self):
        return self.name


class ShareFonds(models.Model):
    share = models.ForeignKey(Share, db_column='idShare', verbose_name='Acción')
    fond = models.ForeignKey(Fond, db_column='idFond', verbose_name='Fondo')
    period = models.ForeignKey(Period, db_column='idPeriod', verbose_name='Periodo')
    minPrice = models.DecimalField(max_digits=10, decimal_places=4, null=True, blank=True, verbose_name='Precio Mínimo')
    maxPrice = models.DecimalField(max_digits=10, decimal_places=4, null=True, blank=True, verbose_name='Precio Máximo')
   
    class Meta:    
        db_table = "ShareFond"
#        ordering = ["fond", "share", "period"]
        verbose_name = "Acciones del Fondo"
        verbose_name_plural = "Acciones de los Fondos"

    def __unicode__(self):
        return self.fond.name + ' - ' + self.share.name  + ' - '  + '{:%d/%m/%Y}'.format(self.period.fromDate) + ' - ' + '{:%d/%m/%Y}'.format(self.period.toDate)


class Alarm(models.Model):
    share = models.ForeignKey(Share, db_column='idShare')
    minPrice = models.DecimalField(max_digits=10, decimal_places=4, blank=True, null=True, verbose_name='Límite Inferior')
    maxPrice = models.DecimalField(max_digits=10, decimal_places=4, blank=True, null=True, verbose_name='Límite Superior')
    changePriceLow = models.DecimalField(max_digits=10, decimal_places=4, blank=True, null=True, verbose_name='Var. Inferior (%)')
    changePriceHigh = models.DecimalField(max_digits=10, decimal_places=4, blank=True, null=True, verbose_name='Var. Superior (%)')
    active = models.BooleanField(blank=False, null=False, default=False)

    class Meta:
        db_table = "Alarm"
        ordering = ["share"]
        verbose_name = "Alarma"
        verbose_name_plural = "Alarmas"      

    def __unicode__(self):
        return self.share.name

