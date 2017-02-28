#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, unicode_literals
from celery import shared_task
from celery import app
from datetime import datetime
from .models import Currency, Share, Alarm
from googleFinance import getShare, getCurrency
import globalVars
from telegramSGP import sendTelegramBot


@shared_task
def updateShares():
    res = True
    try:
        globalVars.toLogFile('updateShares inicio')
        shares = Share.objects.exclude(ticker__isnull=True).exclude(ticker__exact='').exclude(update=False)
        for share in shares:
             try:
                 company = share.ticker
                 shareResult = getShare(company)
                 share.lastValue = shareResult['Value']
                 share.datetime = datetime.strptime(shareResult['Datetime'], '%Y-%m-%dT%H:%M:%S')
                 share.close = shareResult['LastDayClose']
                 share.change = shareResult['Change']
                 share.openValue = shareResult['Open']
                 share.save()
             except Exception as e:
                 res = False
                 globalVars.toLogFile('Error updateShares - share: ' + share.ticker + ' ' + str(e))
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
        return res
    except Exception as e:
        globalVars.toLogFile('Error updateCurrency: ' + str(e))
        return False


def msgAlarm(name, event, change, unity, lastValue):
    msg = 'Cotización ' + name + '. El precio ' + event + ' ' + str(round(change, 1)) + ' ' + unity.lower() + '. Precio actual: ' + str(round(lastValue, 2))  + '\n'
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
                redisAvisada = globalVars.redisAlarmaBolsaYaAvisada.replace('X', share.name)
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
                globalVars.toLogFile('Error alarmCheck - accion: ' + share.ticker + ' ' + str(e))
        if msg:
            sendTelegramBot('ALERTA DE BOLSA! ' + msg)
        globalVars.toLogFile('alarmCheck fin: ' + str(res))
        return True
    except Exception as e:
        #globalVars.toLogFile('Error alarmCheck: ' + str(e))
        return False
