from django.contrib import admin

from gift_card.models import GiftCard, UsedGiftCard


class GiftCardAdmin(admin.ModelAdmin):
    list_display = ['code',  'amount_off', 'type', 'valid', 'buyer']
    search_fields = ['code']
    list_filter = ['valid', 'type',]


admin.site.register(GiftCard, GiftCardAdmin)
admin.site.register(UsedGiftCard)

