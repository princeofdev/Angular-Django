import re
import django_filters

from geo.models import WorkZone
from services.models import Service, CityServices, Category


class ServiceFilter(django_filters.FilterSet):
    type = django_filters.CharFilter(name="type")
    category = django_filters.CharFilter(name="category")
    cities = django_filters.CharFilter(method='filter_city')
    zip = django_filters.CharFilter(method='filter_zip')
    work_zones = django_filters.CharFilter(method='filter_work_zone')

    class Meta:
        model = Service
        fields = ['type', 'category']

    def filter_city(self, queryset, name, value):
        services = CityServices.objects.filter(city=value).values_list('service', flat=True)
        return queryset.filter(pk__in=services)

    def filter_zip(self, queryset, name, value):
        cities = WorkZone.objects.filter(zip_codes__icontains=value).values_list('city', flat=True)
        services = CityServices.objects.filter(city__in=cities).values_list('service', flat=True)
        return queryset.filter(pk__in=services)

    def filter_work_zone(self, queryset, name, value):
        values = re.sub(r'\s', '', value).split(',')
        cities = WorkZone.objects.filter(pk__in=values).values_list('city', flat=True)
        services = CityServices.objects.filter(city__in=cities).values_list('service', flat=True)
        return queryset.filter(pk__in=services)


class CategoryFilter(django_filters.FilterSet):
    cities = django_filters.CharFilter(method='filter_city')
    zip = django_filters.CharFilter(method='filter_zip')

    class Meta:
        model = Category
        fields = ['name',]

    def filter_city(self, queryset, name, value):
        services = CityServices.objects.filter(city=value).values_list('service', flat=True)
        categories = Service.objects.filter(pk__in=services).values_list('category', flat=True)
        return queryset.filter(pk__in=categories)

    def filter_zip(self, queryset, name, value):
        cities = WorkZone.objects.filter(zip_codes__icontains=value).values_list('city', flat=True)
        services = CityServices.objects.filter(city__in=cities).values_list('service', flat=True)
        categories = Service.objects.filter(id__in=services).values_list('category', flat=True)
        return queryset.filter(pk__in=categories)
