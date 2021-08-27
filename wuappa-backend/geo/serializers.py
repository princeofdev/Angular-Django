# -*- coding: utf-8 -*-
from rest_framework import serializers

from geo.models import Country, City, Region, WorkZone


class CountrySerializer(serializers.ModelSerializer):

    class Meta:
        model = Country
        fields = ('id', 'name')


class RegionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Region
        fields = ('id', 'name')


class CitySerializer(serializers.ModelSerializer):

    class Meta:
        model = City
        fields = ('id', 'name')


class WorkZoneSerializer(serializers.ModelSerializer):

    class Meta:
        model = WorkZone
        fields = ('id', 'name', 'city')
