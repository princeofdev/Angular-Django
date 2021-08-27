from rest_framework import viewsets, mixins

from geo.models import Country, Region, City, WorkZone
from geo.serializers import CountrySerializer, RegionSerializer, CitySerializer, WorkZoneSerializer


class CountryViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    List of countries
    """
    queryset = Country.objects.filter(status=Country.STATUS.ACTIVE).order_by('name')
    serializer_class = CountrySerializer
    permission_classes = ()
    pagination_class = None
    search_fields = ('name', 'alternative_names')


class RegionViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    List of regions
    """
    queryset = Region.objects.filter(
        country__status=Country.STATUS.ACTIVE, status=Region.STATUS.ACTIVE
    ).order_by('name')
    serializer_class = RegionSerializer
    permission_classes = ()
    pagination_class = None
    filter_fields = ('country',)
    search_fields = ('name',)


class CityViewSet(mixins.RetrieveModelMixin,
                  mixins.ListModelMixin,
                  viewsets.GenericViewSet):
    """
    List of cities
    """
    queryset = City.objects.filter(
        country__status=Country.STATUS.ACTIVE,
        region__status=Region.STATUS.ACTIVE,
        status=City.STATUS.ACTIVE
    ).order_by('name')
    serializer_class = CitySerializer
    permission_classes = ()
    pagination_class = None
    filter_fields = ('region', 'country')
    search_fields = ('name',)


class WorkZoneViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    List of work zones
    """
    queryset = WorkZone.objects.filter(
        city__country__status=Country.STATUS.ACTIVE,
        city__region__status=Region.STATUS.ACTIVE,
        city__status=City.STATUS.ACTIVE,
        status=WorkZone.STATUS.ACTIVE
    ).order_by('name')
    serializer_class = WorkZoneSerializer
    permission_classes = ()
    filter_fields = ('city', 'city__region', 'city__country')
    search_fields = ('name',)
