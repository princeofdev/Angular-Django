from allauth.account.models import EmailAddress
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from django.utils.html import format_html
from django.utils.translation import ugettext as _
from rest_framework.authtoken.models import Token

from profiles.filters import UserWorkZoneCountryFilter, UserWorkZoneCityFilter, UserWorkZoneRegionFilter, \
    UserWorkZoneFilter
from profiles.models import Profile, UserWorkZone
from profiles.settings import PROFILE_TYPE, PROFESSIONAL, FINAL
from services.admin import CustomerHireServiceInline, ProfessionalHireServiceInline
from services.models import UserService


class ProfileUserInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = _('Profiles')
    exclude = ('city', 'documents')
    extra = 0
    readonly_fields = ['get_documents_link']

    def get_fields(self, request, obj=None):
        if obj.profile.type == PROFESSIONAL:
            return super(ProfileUserInline, self).get_fields(request, obj)
        else:
            return 'type', 'phone', 'picture', 'language'

    def get_documents_link(self, obj):
        if obj.documents:
            html = ''
            for doc in obj.documents:
                html += '<a href="' + doc + '" target="_blank">' + doc + '</a><br>'
            return format_html(html)
    get_documents_link.short_description = 'Documents'
    get_documents_link.allow_tags = True


class UserWorkZoneInLine(admin.StackedInline):
    model = UserWorkZone
    extra = 0


class UserServiceInline(admin.StackedInline):
    model = UserService
    extra = 0


class UserAdmin(BaseUserAdmin):
    list_display = ['id', 'first_name', 'last_name', 'email', 'profile_phone', 'profile_type', 'is_active', 'is_verify',
                    'profile_rating']
    list_filter = ['profile__type', 'is_active', 'emailaddress__verified', UserWorkZoneCountryFilter,
                   UserWorkZoneRegionFilter, UserWorkZoneCityFilter, UserWorkZoneFilter]
    search_fields = ['first_name', 'last_name', 'email', 'profile__phone']
    inlines = (ProfileUserInline, UserWorkZoneInLine, UserServiceInline, CustomerHireServiceInline,
               ProfessionalHireServiceInline)
    # To change add_user fields
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2'),
        }),
    )

    fieldsets = (
        (_('User data'), {
            'fields': ('first_name', 'last_name', 'email', 'password', 'is_active')
        }),
        (_('Groups & permissions'), {
            'fields': ('is_superuser', 'is_staff', 'groups', 'user_permissions'),
            'classes': ('collapse',)
        }),
    )

    def get_formsets_with_inlines(self, request, obj=None):
        if obj:
            try:
                for inline in self.get_inline_instances(request, obj):
                    if obj.profile.type == PROFESSIONAL and isinstance(inline, CustomerHireServiceInline):
                        continue
                    if obj.profile.type == FINAL and (
                            isinstance(inline, ProfessionalHireServiceInline) or
                            isinstance(inline, UserWorkZoneInLine) or isinstance(inline, UserServiceInline)
                    ):
                        continue
                    yield inline.get_formset(request, obj), inline
            except Profile.DoesNotExist:
                # When create an user from django admin. Only for create Superusers
                obj.is_superuser = True
                obj.is_staff = True
                Profile.objects.create(user=obj)
                obj.save()

    def profile_phone(self, obj):
        return obj.profile.phone

    profile_phone.short_description = _("Phone")
    profile_phone.admin_order_field = 'profile__phone'

    def profile_type(self, obj):
        tuple_to_dict = dict(PROFILE_TYPE)
        return tuple_to_dict[obj.profile.type]

    profile_type.short_description = _("Type")
    profile_type.admin_order_field = 'profile__type'

    def profile_rating(self, obj):
        return obj.profile.rating

    profile_rating.short_description = _("Rating")
    profile_rating.admin_order_field = 'profile__rating'

    def is_verify(self, obj):
        try:
            user_verify = EmailAddress.objects.get(user_id=obj.id)
            return user_verify.verified
        except EmailAddress.DoesNotExist:
            return False

    is_verify.short_description = _("Is Verified")
    is_verify.boolean = True


admin.site.unregister(Token)
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
