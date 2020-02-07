import _thread
from django.shortcuts import render
from datetime import datetime

from finance import getShare, getCurrency
from sharesWebApp.models import Share, Currency

import globalVars


def inicio(request, notifMsg=''):
    sharesResult = []
    shares = Share.objects.exclude(ticker__isnull=True).exclude(ticker__exact='').exclude(update=False)
    for share in shares:
        try:
            company = share.ticker
            # shareResult = getShare(company)
            # share.lastValue = shareResult['Value']
            # share.datetime = datetime.strptime(shareResult['Datetime'], '%Y-%m-%dT%H:%M:%S')
            # share.save()
            shareResult['Name'] = share.name
            shareResult['Value'] = share.lastValue
            shareResult['Datetime'] = share.datetime
            sharesResult.append(shareResult)
        except Exception as e:
            globalVars.toLogFile('Error inicio: ' + str(e))

    currencysResult = []
    currencys = Currency.objects.all().exclude(ticker__isnull=True).exclude(ticker__exact='').exclude(update=False)
    for currency in currencys:
        try:
            # c = currency.ticker
            # currencyResult = getCurrency(c)
            # currency.euro = currencyResult['Value']
            # currency.datetime = datetime.strptime(currencyResult['Datetime'], '%Y-%m-%d %H:%M:%S')
            # currency.save()
            currencyResult['Name'] = currency.name
            currencysResult.append(currencyResult)
        except Exception as e:
            globalVars.toLogFile('Error inicio: ' + str(e))

    values = {'shares': sharesResult, 'currencys': currencysResult}
    return render(request, 'inicio.html', values)
