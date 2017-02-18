from yahoo_finance import Share
from yahoo_finance import Currency

yahoo = Share('BBVA')
print('Open: ' + str(yahoo.get_open()))
print('Actual: ' + str(yahoo.get_price()))
#print(yahoo.get_trade_datetime())
print(yahoo.get_prev_close())
#print(yahoo.get_stock_exchange())
# print('Fecha Actual: ' + str(yahoo.get_trade_datetime()))
# yahoo.refresh()


# eur_usd = Currency('EURUSD')
# print('1 EUR = ' + str(eur_usd.get_rate() + ' USD'))

# usd_eur = Currency('USDEUR')
# print('1 USD = ' + str(usd_eur.get_rate() + ' EUR'))

# eur_rub = Currency('EURRUB')
# print('1 EUR = ' + str(eur_rub.get_rate() + ' RUBLOS'))

# eur_lib = Currency('EURGBP')
# print('1 EUR = ' + str(eur_lib.get_rate() + ' GBP'))
