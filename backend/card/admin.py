from django.contrib import admin

from card.models import Card


class CardAdmin(admin.ModelAdmin):
    list_display = ('account',
                    'is_active',
                    'number',
                    'expires_date',
                    'code',
                    'pin',
                    'daily_online_limit',
                    'daily_withdrawal_limit',
                    'monthly_online_limit',
                    'monthly_withdrawal_limit'
                    )
    list_filter = ('is_active', )
    fieldsets = (
        ('Card account', {'fields': ('account', )}),
        ('Card info', {'fields': ('is_active', 'number', 'expires_date', 'code', 'pin')}),
        ('Card limit', {'fields': ('daily_online_limit',
                                   'daily_withdrawal_limit',
                                   'monthly_online_limit',
                                   'monthly_withdrawal_limit')})
    )
    search_fields = ('account', 'number')
    ordering = ('account', )
    filter_horizontal = ()


admin.site.register(Card, CardAdmin)
