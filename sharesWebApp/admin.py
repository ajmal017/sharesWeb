from django.contrib import admin
from models import Currency, Index, Period, Fond, Share, Alarm, ShareFonds

class CurrencyAdmin(admin.ModelAdmin):
    list_display = ('name', 'symbol')
    search_fields = ('name', )
    ordering = ('name',)

class IndexAdmin(admin.ModelAdmin):
    list_display = ('name', )
    search_fields = ('name', )
    ordering = ('name',)


class PeriodAdmin(admin.ModelAdmin):
    list_display = ('fromDate', 'toDate')
    search_fields = ('fromDate', 'toDate')
    date_hierarchy = 'fromDate'
    ordering = ('fromDate',)


class FondAdmin(admin.ModelAdmin):
    list_display = ('name', )
    search_fields = ('name', )
    ordering = ('name',)

class ShareAdmin(admin.ModelAdmin):
    list_display = ('name', 'ISIN', 'index', 'ticker')
    search_fields = ('name', 'ISIN', 'ticker')
    ordering = ('name',)

class AlarmAdmin(admin.ModelAdmin):
    list_display = ('share', 'minPrice', 'maxPrice', 'changePriceLow', 'changePriceHigh', 'active')
    search_fields = ('share', )
    ordering = ('share',)
    raw_id_fields = ('share',)

class ShareFondsAdmin(admin.ModelAdmin):
    list_display = ('share', 'fond', 'period')
    search_fields = ('share', 'fond', 'period')
    ordering = ('share',)
    raw_id_fields = ('share', )


# Register your models here.
admin.site.register(Currency, CurrencyAdmin)
admin.site.register(Index, IndexAdmin)
admin.site.register(Period, PeriodAdmin)
admin.site.register(Fond, FondAdmin)
admin.site.register(Share, ShareAdmin)
admin.site.register(Alarm, AlarmAdmin)
admin.site.register(ShareFonds, ShareFondsAdmin)
