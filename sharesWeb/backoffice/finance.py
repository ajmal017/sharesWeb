import globalVars
import pycurl
import json
from io import BytesIO
from yahoo_finance import Share, Currency
from datetime import datetime
from pandas_datareader import data
import pandas as pd


def getShareGoogle(identifier):
    try:
        get_value_url = 'http://finance.google.com/finance/info?client=ig&q=' + identifier
        buffer = BytesIO()
        c = pycurl.Curl()
        c.setopt(c.URL, get_value_url)
        c.setopt(c.WRITEDATA, buffer)
        c.perform()
        c.close()
        value = buffer.getvalue()
        value = value.decode('utf-8')
        # print(value)
        j = json.loads(value[5:len(value) - 2])
        share_value = float(j['l'].replace(',', ''))
        share_lastDayClose = float(j['pcls_fix'])
        share_change = ((share_value / share_lastDayClose) -1) * 100  # El resultado se devuelve en %
        dt = j['lt_dts']
        dt = dt[:-1]
        # share_volume = float(j['vo'])
        share_volume = 0
        share = {'Name': j['t'], 'Index': j['e'], 'Open': float(j['pcls_fix']), 'Value': share_value, 'Datetime': dt, 'Change': share_change, 'LastDayClose': share_lastDayClose, 'Volume': share_volume}
        return share
    except Exception as e:
        globalVars.toLogFile('Error getShareGoogle: ' + str(e))
        return None


def getShareYahoo(identifier):
    try:
        share = Share(identifier)
        open = float(share.get_open())
        value = float(share.get_price()) 
        change = float(share.get_percent_change().replace('%',''))
        volume = float(share.get_volume())
        prev_close = float(share.get_prev_close())
        sh = {'Name': share.get_name(), 'Index': share.get_stock_exchange(), 'Open': open, 'Value': value, 'Datetime': share.get_trade_datetime(), 'Change': change, 'LastDayClose': prev_close, 'Volume': volume}
        return sh
    except Exception as e:
        globalVars.toLogFile('Error getShareYahoo: ' + str(e))
        return None


def getShare(identifier, google=True):
    if google:
        return getShareGoogle(identifier)
    else:
        return getShareYahoo(identifier)


def getCurrency(identifier):
    try:
        result = Currency(identifier)
        dt = result.get_trade_datetime()[:-9]
        value = float(result.get_rate())
        #lastDayClose = result.get_prev_close()
        lastDayClose = value
        #open = result.get_open()
        open = value
        cur_change = ((value / lastDayClose) -1) * 100  # El resultado se devuelve en %
        currency = {'Name': identifier, 'Value': value, 'Datetime': dt, 'Open': open, 'Change': cur_change, 'LastDayClose': lastDayClose}
        return currency
    except Exception as e:
        globalVars.toLogFile('Error getCurrency: ' + str(e))
        return None


# if __name__ == "__main__":
#      company = 'BME:TEF'
#      share = getShareGoogle(company)
#      if share:
#          print('Ticker: ' + share['Name'])
#          print('UltimoValor: %.2f' % share['LastDayClose'])
#          print('Actual: %.2f' % share['Value'])
#          print('Fecha: ' + share['Datetime'])
#          print('Var: %.2f' % share['Change'] + '%')
#          print('Open: %.2f' % share['Open'])
#          print('')

#      currency = 'EURUSD'
#      cur = getCurrency(currency)
#      if cur:
#          print('Name: ' + cur['Name'])
#          print('UltimoValor: %.4f' % cur['LastDayClose'])
#          print('Actual: %.4f' % cur['Value'])
#          print('Fecha: ' + cur['Datetime'])
#          print('Var: %.4f' % cur['Change'] + '%')
#          print('Open: %.4f' % cur['Open'])
