#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, unicode_literals
from django.utils import timezone
from celery import shared_task
from celery import app
from datetime import datetime, timedelta, date
from .models import Currency, Share, Alarm, Summary, Transaction, ShareHistory, DepositWithdraw, CurrencyHistory, calcProfitability
from django.db.models import Q
from finance import getShare, getCurrency
from forex_python.converter import CurrencyRates
from pandas_datareader import data
#from pandas_datareader.oanda import get_oanda_currency_historical_rates
from pandas_datareader.fred import FredReader
import pandas as pd
from decimal import Decimal
import globalVars


@shared_task
def updateShares():
    res = True
    try:
        globalVars.toLogFile('updateShares inicio')
        shares = Share.objects.exclude(tickerGoogle__isnull=True).exclude(tickerGoogle__exact='').exclude(update=False)
        for share in shares:
             try:
                 company = share.tickerGoogle
                 shareResult = getShare(company)
                 share.lastValue = shareResult['Value']
                 share.datetime = datetime.strptime(shareResult['Datetime'], '%Y-%m-%dT%H:%M:%S')
                 share.close = shareResult['LastDayClose']
                 share.change = shareResult['Change']
                 share.openValue = shareResult['Open']
                 share.save()
             except Exception as e:
                 res = False
                 globalVars.toLogFile('Error updateShares - share: ' + share.tickerGoogle + ' ' + str(e))
        globalVars.toLogFile('updateShares fin: ' + str(res))
        alarmCheck()
        return res
    except Exception as e:
        globalVars.toLogFile('Error updateShares: ' + str(e))
        return False


@shared_task
def updateCurrency():
    res = True
    try:
        globalVars.toLogFile('updateCurrency inicio')
        currencys = Currency.objects.exclude(ticker__isnull=True).exclude(ticker__exact='').exclude(update=False)
        for currency in currencys:
            try:
                c = currency.ticker
                currencyResult = getCurrency(c)
                currency.lastValue = currencyResult['Value']
                currency.datetime = datetime.strptime(currencyResult['Datetime'], '%Y-%m-%d %H:%M:%S')
                currency.close = currencyResult['LastDayClose']
                currency.change = currencyResult['Change']
                currency.openValue = currencyResult['Open']
                currency.save()
            except Exception as e:
                res = False
                globalVars.toLogFile('Error updateCurrency - currency: ' + currency.ticker + ' ' + str(e))
        globalVars.toLogFile('updateCurrency fin: ' + str(res))
        calcSummary()
        return res
    except Exception as e:
        globalVars.toLogFile('Error updateCurrency: ' + str(e))
        return False


def msgAlarm(name, event, change, unity, lastValue):
    msg = 'Cotizacion ' + name + '. El precio ' + event + ' ' + str(round(change, 1)) + ' ' + unity.lower() + '. Precio actual: ' + str(round(lastValue, 2))  + '\n'
    return msg


@shared_task
def alarmCheck():
    try:
        globalVars.toLogFile('alarmCheck inicio')
        res = True
        msg = ''
        alarms = Alarm.objects.exclude(active=False)
        for alarm in alarms:
            try:
                share = alarm.share
                avisar = False
                redisAvisada = globalVars.redisAlarmaBolsaYaAvisada.replace('X', share.tickerGoogle)
                if (alarm.changePriceLow is not None) and (share.change is not None) and (not globalVars.redisGet(redisAvisada)):
                    if (share.change <= alarm.changePriceLow):
                        msg = msg + msgAlarm(share.name, 'ha bajado', share.change, '%', share.lastValue)
                        avisar = True
                if (alarm.changePriceHigh is not None) and (share.change is not None) and (not globalVars.redisGet(redisAvisada)):
                    if (share.change >= alarm.changePriceHigh):
                        msg = msg + msgAlarm(share.name, 'ha subido', share.change, '%', share.lastValue)
                        avisar = True
                if (alarm.minPrice is not None) and (share.lastValue is not None) and (not globalVars.redisGet(redisAvisada)):
                    if (alarm.minPrice >= share.lastValue):
                        msg = msg + msgAlarm(share.name, 'es inferior a ', alarm.minPrice, share.currency.symbol, share.lastValue)
                        avisar = True
                if (alarm.maxPrice is not None) and (share.lastValue is not None) and (not globalVars.redisGet(redisAvisada)):
                    if (alarm.maxPrice <= share.lastValue):
                        msg = msg + msgAlarm(share.name, 'es superior a ', alarm.maxPrice, share.currency.symbol, share.lastValue)
                        avisar = True
                if avisar:
                    globalVars.redisSet(redisAvisada, redisAvisada, 36000)
            except Exception as e:
                res = False
                globalVars.toLogFile('Error alarmCheck - accion: ' + share.tickerGoogle + ' ' + str(e))
        if msg:
            #sendTelegramBot('ALERTA DE BOLSA! ' + msg)
            globalVars.toFile(globalVars.sendFile, 'ALERTA DE BOLSA! ' + msg)
        globalVars.toLogFile('alarmCheck fin: ' + str(res))
        return res
    except Exception as e:
        globalVars.toLogFile('Error alarmCheck: ' + str(e))
        return False


@shared_task
def calcSummary():
    try:
        globalVars.toLogFile('calcSummary inicio')
        res = True
        today = timezone.now().date()
        today =  today +timedelta(days=-2)
        # setAllShareHistory(today, today)
        # setCurrencyHistory(today, today)
        setSummaryHistory(today)
        # setAllNewShareHistory()
        globalVars.toLogFile('calcSummary fin')
        return res
    except Exception as e:
        globalVars.toLogFile('Error calcSummary: ' + str(e))
        return False


def setShareHistory(tickYahoo, startDate, endDate):
    try:
        s = Share.objects.get(tickerYahoo=tickYahoo)
        ok = False
        retries = 5
        while (retries > 0)  and (not ok):
            try:
                p = data.DataReader(tickYahoo, 'yahoo', startDate, endDate)
                ok = True
            except Exception as e:
                retries = retries - 1
        if not ok:
            raise Exception('Error intentando obtener histórico acción ' + tickYahoo + ' con pandas')
        daterange = pd.date_range(startDate, endDate)
        for single_date in daterange:
            try:
                sh = p.ix[single_date]
                try:
                    hist = ShareHistory.objects.get(share=s, date=single_date)
                except ShareHistory.DoesNotExist:
                    hist = ShareHistory()
                hist.share = s
                hist.date = single_date
                hist.open = sh[0]
                hist.high = sh[1]
                hist.low = sh[2]
                hist.close = sh[3]
                hist.volume = sh[4]
                hist.save()
            except Exception as e:
                pass
        return True
    except Exception as e:
        globalVars.toLogFile('Error getShareHistory: ' + str(e))
        return False


def setAllShareHistory(startDate, endDate):
    try:
        shs = Share.objects.all()
        for sh in shs:
            ticker = sh.tickerYahoo
            setShareHistory(ticker, startDate, endDate)
        return True
    except Exception as e:
        globalVars.toLogFile('Error setAllShareHistory: ' + str(e))
        return False


def setAllNewShareHistory():
    try:
        startDate = date(2006,1,1)
        endDate = timezone.now().date()
        shs = Share.objects.all()
        for sh in shs:
            #if (ShareHistory.objects.filter(share = sh).count() == 0):
            if (True):
                ticker = sh.tickerYahoo
                setShareHistory(ticker, startDate, endDate)
        return True
    except Exception as e:
        globalVars.toLogFile('Error setAllNewShareHistory: ' + str(e))
        return False


def setCurrencyHistory(startDate, endDate):
    try:
        daterange = pd.date_range(startDate, endDate)
        for single_date in daterange:
            try:
                ok = False
                retries = 5
                while (retries > 0)  and (not ok):
                    try:
                        cur = CurrencyRates()
                        rates = cur.get_rates('EUR', single_date)
                        ok = True
                    except Exception as e:
                        retries = retries - 1
                if not ok:
                    raise Exception('Error intentando obtener histórico divisas ' + c.symbol)
                currencies = Currency.objects.filter(update=True)
                for c in currencies:
                    try:
                        value = rates[c.symbol]
                        try:
                            hist = CurrencyHistory.objects.get(currency=c, date=single_date)
                        except CurrencyHistory.DoesNotExist:
                            hist = CurrencyHistory()
                        hist.currency = c
                        hist.date = single_date
                        hist.close = value
                        hist.save()
                    except Exception as e:
                        globalVars.toLogFile('Error setCurrencyHistory: ' + str(e))
            except Exception as e:
                globalVars.toLogFile('Error setCurrencyHistory: ' + str(e))
                # pass
        return True
    except Exception as e:
        globalVars.toLogFile('Error setCurrencyHistory: ' + str(e))
        return False


def setSummaryHistory(dateCalc):
    try:
        if dateCalc.weekday() > 4:  # Weekend: we don't calculate summary
            globalVars.toLogFile('setSummaryHistory: el día seleccionado es festivo')
            return True
        res = True

        totalBuy = 0
        totalSell = 0
        totalDividend = 0
        totalRights = 0
        totalProfit = 0
        currentBuy = 0
        currentSell = 0
        currentDividend = 0
        currentRights = 0
        currentProfit = 0
        #transacs = Transaction.objects.filter(Q(dateSell__isnull=True) | Q(dateSell__gte=dateCalc), dateBuy__lte=dateCalc).order_by('dateBuy', 'dateSell')
        transacs = Transaction.objects.filter(dateBuy__lte=dateCalc).order_by('dateBuy', 'dateSell')
        for transac in transacs:
            if (not transac.dateSell) or (transac.dateSell > dateCalc):
                transac.priceSellUnity = 0
                transac.sharesSell = 0
                transac.comissionSell = 0
                transac.share.currency.lastValue = transac.share.currency.getValueAtDate(dateCalc)
                transac.share.lastValue = transac.share.getValueAtDate(dateCalc)

            iterPriceBuy = transac.priceBuyTotal
            iterPriceSell = transac.priceSellTotal
            iterDividend = transac.getDividend(True, dateCalc)
            iterRights = transac.getRights(dateCalc)
            iterProfit = transac.getProfit(dateCalc)
            if (not transac.dateSell) or (transac.dateSell > dateCalc):
                currentBuy = currentBuy + iterPriceBuy
                currentSell = currentSell + iterPriceSell
                currentDividend = currentDividend + iterDividend
                currentRights = currentRights + iterRights
                currentProfit = currentProfit + iterProfit
                #globalVars.toLogFile('Accion: ' + transac.share.name + '. Beneficio: ' +str(round(transac.profit,2)))
            totalBuy = totalBuy + iterPriceBuy
            totalSell = totalSell + iterPriceSell
            totalDividend = totalDividend + iterDividend
            totalRights = totalRights + iterRights
            totalProfit = totalProfit + iterProfit

        try:
            summ = Summary.objects.get(date=dateCalc) # Si existe el registro, lo actualizamos
        except Summary.DoesNotExist:
            summ = Summary(date=dateCalc) # En caso contrario, creamos uno nuevo
        summ.priceBuyTotal = totalBuy
        summ.priceSellTotal = totalSell
        summ.dividendGrossTotal = totalDividend
        summ.rightsTotal = totalRights
        summ.profitTotal = totalProfit
        summ.priceBuyCurrent = currentBuy
        summ.priceSellCurrent = currentSell
        summ.dividendGrossCurrent = currentDividend
        summ.rightsCurrent = currentRights
        summ.profitCurrent = currentProfit
        summ.profitabilityCurrent = calcProfitability(currentBuy, currentSell, currentDividend, currentRights, 1)
        summ.save()
        return res
    except Exception as e:
        globalVars.toLogFile('Error setSummaryHistory: ' + str(e))
        return False


def setAllSummaryHistory(startDate, endDate):
    try:
        d = startDate
        delta = timedelta(days=1)
        while d <= endDate:
            setSummaryHistory(d)
            d += delta
        return True
    except Exception as e:
        globalVars.toLogFile('Error setAllSummaryHistory: ' + str(e))
        return False

