from django.contrib import admin
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext as _
from rangefilter.filter import DateRangeFilter

from services.models import Category, Service, CityServices, HireService
from services.settings import COMPLETE
from services.views import ServicesExportReport


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'status']
    list_filter = ['status']
    search_fields = ['name']


class CityServicesInline(admin.StackedInline):
    model = CityServices
    extra = 0


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'category_name', 'status', 'type']
    list_filter = ['status', 'type', 'category']
    search_fields = ['name', 'category__name']
    inlines = [CityServicesInline, ]

    def category_name(self, obj):
        return obj.category.name
    category_name.short_description = _("Category Name")


@admin.register(HireService)
class HireServiceAdmin(admin.ModelAdmin):
    list_display = ['id', 'client_email', 'professional_email', 'date_formatted', 'time_formatted', 'status']
    list_filter = [
        'status', ('date', DateRangeFilter)
    ]
    search_fields = ['client__email', 'client__username', 'professional__email', 'professional__username']

    def client_email(self, obj):
        return obj.client.email
    client_email.short_description = _("Client email")

    def professional_email(self, obj):
        if obj.professional:
            return obj.professional.email
    professional_email.short_description = _("Professional email")

    def date_formatted(self, obj):
        return obj.date.strftime("%d/%m/%Y")
    date_formatted.short_description = _("Date")

    def time_formatted(self, obj):
        return obj.time.strftime("%H:%M")
    time_formatted.short_description = _("Time")


admin.site.register_view('services-export', 'Export services report', view=ServicesExportReport.as_view())


class CustomerHireServiceInline(admin.TabularInline):
    model = HireService
    fields = ('date', 'time', 'status', 'professional', 'address', 'rating', 'review', 'get_link')
    readonly_fields = ('date', 'time', 'status', 'professional', 'address', 'rating', 'review', 'get_link')
    ordering = ('-date', '-time')
    fk_name = 'client'
    extra = 0
    can_delete = False

    def get_link(self, obj):
        return mark_safe('<a href="{0}">View</a>'.format(reverse('admin:services_hireservice_change', args=[obj.pk])))
    get_link.short_description = ''


class ProfessionalHireServiceInline(admin.TabularInline):
    model = HireService
    fields = ('date', 'time', 'status', 'client', 'address', 'rating', 'review', 'get_link')
    readonly_fields = (
    'date', 'time', 'status', 'client', 'address', 'rating', 'review', 'get_link')
    ordering = ('-date', '-time')
    fk_name = 'professional'
    extra = 0
    can_delete = False

    def get_link(self, obj):
        return mark_safe('<a href="{0}">View</a>'.format(reverse('admin:services_hireservice_change', args=[obj.pk])))

    get_link.short_description = ''
