from django.contrib import admin

from coupon.models import Coupon, UsedCoupon


class CouponAdmin(admin.ModelAdmin):
    list_display = ['code',  'amount_off', 'type', 'valid']
    search_fields = ['code']
    list_filter = ['valid', 'type',]


admin.site.register(Coupon, CouponAdmin)
admin.site.register(UsedCoupon)

