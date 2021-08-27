from cities_light.admin import CountryAdmin, RegionAdmin, CityAdmin
from django.contrib import admin
from django.utils.translation import ugettext as _

# Register your models here.
from geo.models import WorkZone, Region, City


# Inlines
class GeoTabularInline(admin.TabularInline):
    list_display_links = ('name')
    fields = ('name', 'status')
    readonly_fields = ('name', 'status')
    can_delete = True
    show_change_link = True
    extra = 0

    def has_add_permission(self, request):
        return False


class RegionInline(GeoTabularInline):
    model = Region
    verbose_name_plural = _('Regions/States')
    extra = 0


class CityInline(GeoTabularInline):
    model = City
    verbose_name_plural = _('Cities')
    extra = 0


class WorkZoneInline(GeoTabularInline):
    model = WorkZone
    verbose_name_plural = _('Work zones')
    extra = 0


# Country admin customization
CountryAdmin.list_display = CountryAdmin.list_display + ('status',)
CountryAdmin.list_filter = CountryAdmin.list_filter + ('status',)
CountryAdmin.inlines = (RegionInline,)

# Region admin customization
RegionAdmin.list_display = RegionAdmin.list_display + ('status',)
RegionAdmin.list_filter = RegionAdmin.list_filter + ('status',)
RegionAdmin.inlines = (CityInline,)

# City admin customization
CityAdmin.list_display = CityAdmin.list_display + ('status',)
CityAdmin.list_filter = CityAdmin.list_filter + ('status',)
CityAdmin.search_fields = CityAdmin.search_fields + ('name', 'region__name', 'country__name')
CityAdmin.inlines = (WorkZoneInline,)


@admin.register(WorkZone)
class WorkZoneAdmin(admin.ModelAdmin):

    def get_region(self, obj):
        return obj.city.region
    get_region.short_description = _('Region/State')
    get_region.admin_order_field = 'city__region'

    def get_country(self, obj):
        return obj.city.country
    get_country.short_description = _('Country')
    get_country.admin_order_field = 'city__country'

    list_display = ('name', 'city', 'get_region', 'get_country', 'status')
    list_filter = ('city', 'city__region', 'city__country', 'status')
    search_fields = ('name', 'city__name', 'city__region__name', 'city__country__name')
