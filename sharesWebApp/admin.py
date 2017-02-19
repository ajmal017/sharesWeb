from django.contrib import admin
from models import Currency, Broker, Index, Period, Fond, Share, Alarm, ShareFonds
from models import Transaction, Dividend


class CurrencyAdmin(admin.ModelAdmin):
    list_display = ('name', 'symbol', 'ticker', 'lastValue', 'datetime')
    search_fields = ('name', )


class BrokerAdmin(admin.ModelAdmin):
    list_display = ('name', )
    search_fields = ('name', )


class IndexAdmin(admin.ModelAdmin):
    list_display = ('name', )
    search_fields = ('name', )


class PeriodAdmin(admin.ModelAdmin):
    list_display = ('fromDate', 'toDate')
    search_fields = ('fromDate', 'toDate')
    date_hierarchy = 'fromDate'


class FondAdmin(admin.ModelAdmin):
    list_display = ('name', )
    search_fields = ('name', )


class ShareAdmin(admin.ModelAdmin):
    list_display = ('name', 'ISIN', 'index', 'ticker', 'update', 'lastValue', 'datetime')
    search_fields = ('name', 'ISIN', 'ticker')


class AlarmAdmin(admin.ModelAdmin):
    list_display = ('share', 'minPrice', 'maxPrice', 'changePriceLow', 'changePriceHigh', 'active')
    search_fields = ('share', )
    raw_id_fields = ('share',)


class ShareFondsAdmin(admin.ModelAdmin):
    list_display = ('share', 'fond', 'period')
    search_fields = ('share', 'fond', 'period')
    raw_id_fields = ('share', )


class TransactionAdmin(admin.ModelAdmin):
    list_display = ('dateBuy','share','sharesBuy','priceBuyTotal','priceSellTotal','dividendGross','profit','profitability')
    search_fields = ('share', )
    raw_id_fields = ('share', )
    date_hierarchy = 'dateBuy'


class DividendAdmin(admin.ModelAdmin):
    list_display = ('date', 'transaction', 'importGross', 'importNet')
    search_fields = ('transaction', 'date')
    raw_id_fields = ('transaction', )
    date_hierarchy = 'date'


# Register your models here.
admin.site.register(Currency, CurrencyAdmin)
admin.site.register(Broker, BrokerAdmin)
admin.site.register(Index, IndexAdmin)
admin.site.register(Period, PeriodAdmin)
admin.site.register(Fond, FondAdmin)
admin.site.register(Share, ShareAdmin)
admin.site.register(Alarm, AlarmAdmin)
admin.site.register(ShareFonds, ShareFondsAdmin)
admin.site.register(Transaction, TransactionAdmin)
admin.site.register(Dividend, DividendAdmin)
