from django.contrib import admin

from transfer.models import Transfer


class TransferAdmin(admin.ModelAdmin):
    list_display = ('sender',
                    'receiver',
                    'title',
                    'amount',
                    'currency',
                    'reference',
                    'status',
                    'method',
                    )
    list_filter = ('method', 'status')
    search_fields = ('sender', 'receiver', 'title')
    ordering = ('created', )
    filter_horizontal = ()


admin.site.register(Transfer, TransferAdmin)
