from django.contrib import admin
from django.utils.translation import ugettext as _

from smsverification.models import VerificationCode


@admin.register(VerificationCode)
class VerificationCodeAdmin(admin.ModelAdmin):

    list_display = ('phone', 'code', 'verified_status', 'expired_status')
    search_fields = ('phone', 'code')

    def verified_status(self, obj):
        return obj.is_verified()
    verified_status.label = _("Verified")
    verified_status.short_description = _("Verified")
    verified_status.admin_order_field = "verification_date"
    verified_status.boolean = True

    def expired_status(self, obj):
        return obj.is_expired()
    expired_status.label = _("Expired")
    expired_status.short_description = _("Expired")
    expired_status.admin_order_field = "expiration_date"
    expired_status.boolean = True
