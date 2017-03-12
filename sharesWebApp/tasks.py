#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, unicode_literals
from django.utils import timezone
from celery import shared_task
from celery import app
from datetime import datetime
from .models import Currency, Share, Alarm, Summary, Transaction, ShareHistory
from finance import getShare, getCurrency
from pandas_datareader import data
import pandas as pd
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
        try:
            summ = Summary.objects.get(date=today)
        except Summary.DoesNotExist:
            summ = Summary(date=today)
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
        transacs = Transaction.objects.all()
        for transac in transacs:
            if not transac.priceSellUnity:
                currentBuy = currentBuy + transac.priceBuyTotal
                currentSell = currentSell + transac.priceSellTotal
                currentDividend = currentDividend + transac.dividendGross
                currentRights = currentRights + transac.rights
                currentProfit = currentProfit + transac.profit
                #globalVars.toLogFile('Accion: ' + transac.share.name + '. Beneficio: ' +str(round(transac.profit,2)))
            totalBuy = totalBuy + transac.priceBuyTotal
            totalSell = totalSell + transac.priceSellTotal
            totalDividend = totalDividend + transac.dividendGross
            totalRights = totalRights + transac.rights
            totalProfit = totalProfit + transac.profit
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
        summ.save()
        globalVars.toLogFile('calcSummary fin: ' + str(res))
        return res
    except Exception as e:
        globalVars.toLogFile('Error calcSummary: ' + str(e))
        return False


def setShareHistory(tickYahoo, startDate, endDate):
    try:
        s = Share.objects.get(tickerYahoo=tickYahoo)        
        p = data.DataReader(tickYahoo, 'yahoo', startDate, endDate)
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
                # hist.close = 
                hist.save()
            except Exception as e:
                pass
        return True
    except Exception as e:
        globalVars.toLogFile('Error getShareHistory: ' + str(e))
        return False


def setAllShareHistory():
    try:
        trs = Transaction.objects.all()
        for tr in trs:
            ticker = tr.share.tickerYahoo
            setShareHistory(ticker, '2015/01/01', '2017/03/09') 
        return True        
    except Exception as e:
        globalVars.toLogFile('Error getShareHistory: ' + str(e))
        return False

