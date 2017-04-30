#!/usr/bin/env python
# -*- coding: utf-8 -*-

#from django.core.urlresolvers import reverse
from django.utils.html import format_html
from django.contrib import admin
from models import Currency, Broker, Index, Period, Fond, Share, ShareHistory
from models import Alarm, ShareFonds, Transaction, Dividend, Right
from models import DepositWithdraw, BrokerComissions, Summary, ShareHistory
from models import CurrencyHistory, ShareType, Sector
from import_export import resources
from import_export.admin import ImportExportModelAdmin


class CurrencyAdmin(admin.ModelAdmin):
    list_display = ('name', 'symbol', 'ticker', 'lastValue', 'datetime', 'close', 'change', 'openValue')
    search_fields = ('name', )


class CurrencyHistoryAdmin(admin.ModelAdmin):
    list_display = ('currency', 'date', 'close', 'change')
    search_fields = ('name', )
    raw_id_fields = ('currency', )
    date_hierarchy = 'date'


class BrokerAdmin(admin.ModelAdmin):
    list_display = ('name', )
    search_fields = ('name', )


class ShareTypeAdmin(admin.ModelAdmin):
    list_display = ('name', )
    search_fields = ('name', )


class SectorAdmin(admin.ModelAdmin):
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
    list_display = ('name', 'ISIN', 'index', 'shareType', 'sector', 'targetValue', 'lastValue', 'datetime', 'close', 'change', 'openValue')
    search_fields = ('name', 'ISIN', 'ticker')


class ShareHistoryAdmin(admin.ModelAdmin):
    list_display = ('share','date','open','close','high','low','change','volume')
    search_fields = ('share', 'date')
    raw_id_fields = ('share', )
    date_hierarchy = 'date'


class AlarmAdmin(admin.ModelAdmin):
    list_display = ('share', 'minPrice', 'maxPrice', 'changePriceLow', 'changePriceHigh', 'active')
    search_fields = ('share', )
    raw_id_fields = ('share',)


class ShareFondsAdmin(admin.ModelAdmin):
    list_display = ('share', 'fond', 'period', 'percent', 'lastValue', 'count', 'minPrice', 'maxPrice', 'avgPrice', 'minVolume', 'maxVolume', 'avgVolume', 'favourite')
    search_fields = ('share', 'fond', 'period')
    raw_id_fields = ('share', )


class TransactionAdmin(ImportExportModelAdmin):
    list_display = ('dateBuy','dateSell','share','getShareLastValue','sharesBuy','priceBuyTotal','priceSellTotal','dividendGross','rights','IRPF','profit','profitability')
    search_fields = ('share', )
    raw_id_fields = ('share', )
    date_hierarchy = 'dateBuy'


    def getShareLastValue(self, obj):
        return obj.share.lastValue
    getShareLastValue.short_description = 'Precio'

    # def getShareLink(self, obj):
    #     url = reverse('admin:share_name_changelist')
    #     html = '<a href="{0}?share__id__exact={1}">{2}</a>'
    #     return html.format(url, obj.id, obj.name)
    # getShareLink.allow_tags = True
    # getShareLink.short_description = 'Nositelji'        

#     def link_to_share(self, share):
# https://share.sergutpal.dynu.com/admin/sharesWebApp/share/4/change/
#         link=urlresolvers.reverse("admin:sharesWebApp_b_change", args=[obj.B.id]) #model name has to be lowercase
#         return u'<a href="%s">%s</a>' % (link,obj.B.name)
#     link_to_B.allow_tags=True


class DividendAdmin(admin.ModelAdmin):
    list_display = ('date', 'transaction', 'importGross', 'importNet', 'importGrossEur', 'importNetEur')
    search_fields = ('transaction','date')
    raw_id_fields = ('transaction', )
    date_hierarchy = 'date'


class RightAdmin(admin.ModelAdmin):
    list_display = ('date', 'transaction', 'importGross')
    search_fields = ('transaction','date')
    raw_id_fields = ('transaction', )
    date_hierarchy = 'date'


class DepositWithdrawAdmin(admin.ModelAdmin):
    list_display = ('date', 'broker','amount','description')
    search_fields = ('broker','date')
    date_hierarchy = 'date'


class BrokerComissionsAdmin(admin.ModelAdmin):
    list_display = ('date', 'broker','amount','description')
    search_fields = ('broker','date')
    date_hierarchy = 'date'


class SummaryAdmin(admin.ModelAdmin):
    list_display = ('date','priceBuyCurrent','priceSellCurrent','dividendGrossCurrent','profitabilityCurrent','priceBuyTotal','priceSellTotal','profitTotal','dividendGrossTotal')
    date_hierarchy = 'date'

# Register your models here.
admin.site.register(Currency, CurrencyAdmin)
admin.site.register(CurrencyHistory, CurrencyHistoryAdmin)
admin.site.register(Broker, BrokerAdmin)
admin.site.register(Index, IndexAdmin)
admin.site.register(ShareType, ShareTypeAdmin)
admin.site.register(Sector, SectorAdmin)
admin.site.register(Period, PeriodAdmin)
admin.site.register(Fond, FondAdmin)
admin.site.register(Share, ShareAdmin)
admin.site.register(ShareHistory, ShareHistoryAdmin)
admin.site.register(Alarm, AlarmAdmin)
admin.site.register(ShareFonds, ShareFondsAdmin)
admin.site.register(Transaction, TransactionAdmin)
admin.site.register(Dividend, DividendAdmin)
admin.site.register(Right, RightAdmin)
admin.site.register(DepositWithdraw, DepositWithdrawAdmin)
admin.site.register(BrokerComissions, BrokerComissionsAdmin)
admin.site.register(Summary, SummaryAdmin)
