#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.db import models
from django.utils import timezone
import globalVars


class Currency(models.Model):
    name = models.CharField(max_length=255, blank=False, null=False, verbose_name='Nombre')
    symbol = models.CharField(max_length=10, blank=False, null=False, default='', verbose_name='Símbolo')
    ticker = models.CharField(max_length=20, blank=True, null=True, verbose_name='Ticker')
    lastValue = models.DecimalField(max_digits=10, decimal_places=4, null=True, blank=True, verbose_name='Valor')
    datetime = models.DateTimeField(blank=True, null=True, verbose_name='Actual.')
    close = models.DecimalField(max_digits=10, decimal_places=4, null=True, blank=True, verbose_name='Cierre')
    change = models.DecimalField(max_digits=5, decimal_places=1, null=True, blank=True, verbose_name='Cambio')
    openValue = models.DecimalField(max_digits=10, decimal_places=4, null=True, blank=True, verbose_name='Apertura')
    update = models.BooleanField(blank=False, null=False, verbose_name='Actualizar', default=True)

    class Meta:
        db_table = "Currency"
        ordering = ["name"]
        verbose_name = "Divisa"
        verbose_name_plural = "Divisas"

    def __unicode__(self):
        return self.name


class Broker(models.Model):
    name = models.CharField(max_length=255, blank=False, null=False, verbose_name='Nombre')

    class Meta:
        db_table = "Broker"
        ordering = ["name"]
        verbose_name = "Broker"
        verbose_name_plural = "Brokers"

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
    currency = models.ForeignKey(Currency, db_column='idCurrency', verbose_name='Divisa', default=1)
    index = models.ForeignKey(Index, db_column='idIndex', blank=True, null=True, verbose_name='Mercado')
    ticker = models.CharField(max_length=20, blank=True, null=True, verbose_name='Ticker')
    favourite = models.BooleanField(blank=False, null=False, verbose_name='Favorito')
    description  =  models.CharField(max_length=8000, blank=True, null=True, verbose_name='Descripción')
    fonds = models.ManyToManyField(Fond, through='ShareFonds', through_fields=('share', 'fond'))
    lastValue = models.DecimalField(max_digits=10, decimal_places=4, null=True, blank=True, verbose_name='Valor')
    datetime = models.DateTimeField(blank=True, null=True, verbose_name='Actual.')
    close = models.DecimalField(max_digits=10, decimal_places=4, null=True, blank=True, verbose_name='Cierre')
    change = models.DecimalField(max_digits=5, decimal_places=1, null=True, blank=True, verbose_name='Cambio (%)')
    openValue = models.DecimalField(max_digits=10, decimal_places=4, null=True, blank=True, verbose_name='Apertura')
    update = models.BooleanField(blank=False, null=False, verbose_name='Actualizar', default=True)

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
        verbose_name = "Acciones del Fondo"
        verbose_name_plural = "Acciones de los Fondos"

    def __unicode__(self):
        return self.fond.name + ' - ' + self.share.name  + ' - '  + '{:%d/%m/%Y}'.format(self.period.fromDate) + ' - ' + '{:%d/%m/%Y}'.format(self.period.toDate)


class Transaction(models.Model):
    share = models.ForeignKey(Share, db_column='idShare', verbose_name='Accion')
    dateBuy = models.DateField(blank=False, null=False, verbose_name='Fecha Compra')
    dateSell = models.DateField(blank=True, null=True, verbose_name='Fecha Venta')
    broker = models.ForeignKey(Broker, db_column='idBroker', verbose_name='Broker', default=1)
    sharesBuy = models.IntegerField(null=False, blank=False, verbose_name='Cantidad Compra')
    sharesSell = models.IntegerField(null=True, blank=True, verbose_name='Cantidad Venta')
    priceBuyUnity = models.DecimalField(max_digits=10, decimal_places=4, null=False, blank=False, verbose_name='Precio Unit. Compra')
    priceSellUnity = models.DecimalField(max_digits=10, decimal_places=4, null=True, blank=True, verbose_name='Precio Unit. Venta')
    comissionBuy = models.DecimalField(max_digits=10, decimal_places=4, null=False, blank=False, verbose_name='Comision Compra')
    comissionSell = models.DecimalField(max_digits=10, decimal_places=4, null=True, blank=True, verbose_name='Comision Venta')
    currencyValueBuy = models.DecimalField(max_digits=10, decimal_places=4, null=False, blank=False, verbose_name='Divisa compra',  default=1)
    currencyValueSell = models.DecimalField(max_digits=10, decimal_places=4, null=True, blank=True, verbose_name='Divisa venta',  default=1)

    @property
    def priceBuyTotal(self):
        try:
            if self.pk is not None:
                return round((self.priceBuyUnity * self.sharesBuy * (1 / self.currencyValueBuy)) + self.comissionBuy, 2)
            else:
                return 0
        except Exception as e:
            globalVars.toLogFile('Error priceBuyTotal: ' + str(e))
            return 0
    priceBuyTotal.fget.short_description = u'Precio Compra'

    @property
    def priceSellTotal(self):
        try:
            if self.pk is not None:
                if self.priceSellUnity > 0:
                    return round((self.priceSellUnity * self.sharesSell * (1 / self.currencyValueBuy)) - self.comissionSell, 2)
                else:
                    if (self.currencyValueBuy != 1):
                        currency = self.share.currency.lastValue
                    else:
                        currency = 1
                    if self.sharesSell > 0:
                        numShares = self.sharesSell
                    else:
                        numShares = self.sharesBuy
                    return round((self.share.lastValue * numShares * (1 / currency)) - self.comissionBuy, 2)
            else:
                return 0
        except Exception as e:
            globalVars.toLogFile('Error priceSellTotal: ' + str(e))
            return 0
    priceSellTotal.fget.short_description = u'Precio Venta'

    def getDividend(self, gross=True):
        total = 0
        try:
            if self.pk is not None:
                divs = Dividend.objects.filter(transaction=self.pk)
                for div in divs:
                    if gross:
                        d = div.importGross
                    else:
                        d = div.importNet
                    d = d * (1 / div.currencyValue)
                    total = total + d
            return round(total, 2)
        except Exception as e:
            globalVars.toLogFile('Error getDividend: ' + str(e))
            return 0

    def getRigths(self):
        total = 0
        try:
            if self.pk is not None:
                rights = Right.objects.filter(transaction=self.pk)
                for right in rights:
                    r = right.importGross
                    r = r * (1 / right.currencyValue)
                    total = total + r
            return round(total, 2)
        except Exception as e:
            globalVars.toLogFile('Error getRigths: ' + str(e))
            return 0

    @property
    def dividendGross(self):
        return round(self.getDividend(True), 2)
    dividendGross.fget.short_description = u'Dividendos Bruto'

    @property
    def dividendNet(self):
        return round(self.getDividend(False), 2)
    dividendNet.fget.short_description = u'Dividendos Neto'

    @property
    def rights(self):
        return round(self.getRigths(), 2)
    rights.fget.short_description = u'Derechos'

    @property
    def profit(self):
        try:
            if self.pk is not None:
                return round(self.priceSellTotal + self.dividendGross + self.rights - self.priceBuyTotal, 2)
            else:
                return 0
        except Exception as e:
            globalVars.toLogFile('Error profit: ' + str(e))
            return 0
    profit.fget.short_description = u'Beneficio Bruto'

    @property
    def IRPF(self):
        try:
            if self.pk is not None:
                return round(self.priceSellTotal + self.rights - self.priceBuyTotal, 2)
            else:
                return 0
        except Exception as e:
            globalVars.toLogFile('Error IRPF: ' + str(e))
            return 0
    IRPF.fget.short_description = u'IRPF/Plusv.'

    @property
    def investDays(self):
        try:
            if self.pk is not None:
                if self.dateSell is None:
                    dateTo = timezone.now().date()
                else:
                    dateTo = self.dateSell
                return (dateTo - self.dateBuy).days
            else:
                return 0
        except Exception as e:
            globalVars.toLogFile('Error investDays: ' + str(e))
            return 0
    investDays.fget.short_description = u'Días invertidos'

#    @property
    def investNormalized(self):
        try:
            if self.pk is not None:
                return round(((self.priceBuyTotal * self.investDays) / 365), 2)
            else:
                return 0
        except Exception as e:
            globalVars.toLogFile('Error investNormalized: ' + str(e))
            return 0
#    investNormalized.fget.short_description = u'Invers.Normalizada'

    @property
    def profitability(self):
        try:
            if self.pk is not None:
                pf = self.priceSellTotal + self.dividendGross + self.rights
                po = self.priceBuyTotal
                pf_div_po = pf / po
                t = 1.0 / (float(self.investDays) / 365.0)
                if self.investDays < 365:
                    return round((pf_div_po - 1) * 100.0, 2)
                else:
                    return round((pow(pf_div_po, t) - 1.0) * 100.0, 2)
            else:
                return 0
        except Exception as e:
            globalVars.toLogFile('Error profitability: ' + str(e))
            return 0
    profitability.fget.short_description = u'Rentabilidad(%)'

    class Meta:
        db_table = "Transaction"
        ordering = ["dateBuy"]
        verbose_name = "Transacción"
        verbose_name_plural = "Transacciones"

    def __unicode__(self):
        return '{:%d/%m/%Y}'.format(self.dateBuy) + ' - ' + self.share.name


class Dividend(models.Model):
    transaction = models.ForeignKey(Transaction, db_column='idTransaction', verbose_name='Transacción')
    date = models.DateField(blank=False, null=False, verbose_name='Fecha')
    importGross = models.DecimalField(max_digits=10, decimal_places=4, null=False, blank=False, verbose_name='Bruto')
    importNet = models.DecimalField(max_digits=10, decimal_places=4, null=False, blank=False, verbose_name='Neto')
    currencyValue = models.DecimalField(max_digits=10, decimal_places=4, null=False, blank=False, verbose_name='Divisa',  default=1)

    class Meta:
        db_table = "Dividend"
        ordering = ["date", "transaction"]
        verbose_name = "Dividendos"
        verbose_name_plural = "Dividendos"

    def __unicode__(self):
        return self.transaction.share.name + ' - ' + '{:%d/%m/%Y}'.format(self.date) + ' - ' + self.transaction.broker.name


# Esta clase permite registrar la venta residual de derechos que hacen los brokers cuando nos sobran algunos 
# derechos. La compra de derechos, la gestionamos como compra normal y corriente de acciones normalizando 
# los precios
class Right(models.Model):
    transaction = models.ForeignKey(Transaction, db_column='idTransaction', verbose_name='Transacción')
    date = models.DateField(blank=False, null=False, verbose_name='Fecha')
    importGross = models.DecimalField(max_digits=10, decimal_places=4, null=False, blank=False, verbose_name='Importe')
    currencyValue = models.DecimalField(max_digits=10, decimal_places=4, null=False, blank=False, verbose_name='Divisa',  default=1)

    class Meta:
        db_table = "Right"
        ordering = ["date", "transaction"]
        verbose_name = "Derechos"
        verbose_name_plural = "Derechos"

    def __unicode__(self):
        return self.transaction.share.name + ' - ' + '{:%d/%m/%Y}'.format(self.date) + ' - ' + self.transaction.broker.name


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


class Summary(models.Model):
    date = models.DateField(blank=False, null=False, verbose_name='Fecha')
    priceBuyCurrent = models.DecimalField(max_digits=10, decimal_places=4, null=True, blank=True, verbose_name='Cartera Compra')
    priceSellCurrent = models.DecimalField(max_digits=10, decimal_places=4, null=True, blank=True, verbose_name='Cartera Venta')
    dividendGrossCurrent = models.DecimalField(max_digits=10, decimal_places=4, null=True, blank=True, verbose_name='Cartera Dividendos')
    profitCurrent = models.DecimalField(max_digits=10, decimal_places=4, null=True, blank=True, verbose_name='Cartera Beneficio')
    priceBuyTotal = models.DecimalField(max_digits=10, decimal_places=4, null=True, blank=True, verbose_name='Total Compra')
    priceSellTotal = models.DecimalField(max_digits=10, decimal_places=4, null=True, blank=True, verbose_name='Total Venta')
    dividendGrossTotal = models.DecimalField(max_digits=10, decimal_places=4, null=True, blank=True, verbose_name='Total Dividendos')
    profitTotal = models.DecimalField(max_digits=10, decimal_places=4, null=True, blank=True, verbose_name='Total Beneficio')


    class Meta:
        db_table = "Summary"
        ordering = ["date"]
        verbose_name = "Resumen"
        verbose_name_plural = "Resumen"

    def __unicode__(self):
        return '{:%d/%m/%Y}'.format(self.date)

