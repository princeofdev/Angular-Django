from django.test import TestCase, override_settings
from rest_framework.test import APIClient

from geo.models import Country, Region, City, WorkZone


@override_settings(ROOT_URLCONF='geo.urls')
class ListCountriesAPITestCase(TestCase):

    def setUp(self):
        self.client = APIClient()

        self.active_countries = [
            Country.objects.create(name="Active Country E", status=Country.STATUS.ACTIVE),
            Country.objects.create(name="Active Country D", status=Country.STATUS.ACTIVE)
        ]

        self.inactive_countries = [
            Country.objects.create(name="Inactive Country C", status=Country.STATUS.INACTIVE),
            Country.objects.create(name="Inactive Country B", status=Country.STATUS.INACTIVE),
            Country.objects.create(name="Inactive Country A", status=Country.STATUS.INACTIVE)
        ]

    def test_only_active_countries_are_listed(self):
        response = self.client.get('/1.0/countries/')
        self.assertEqual(len(response.data), len(self.active_countries))

        active_countries_names = list(map(lambda item: item.name, self.active_countries))
        inactive_countries_names = list(map(lambda item: item.name, self.inactive_countries))
        response_names = list(map(lambda item: item.get("name"), response.data))

        for name in response_names:
            self.assertIn(name, active_countries_names)

        for name in response_names:
            self.assertNotIn(name, inactive_countries_names)

    def test_countries_are_listed_alphabetically(self):
        response = self.client.get('/1.0/countries/')
        response_names = list(map(lambda item: item.get("name"), response.data))
        active_countries_names_ordered_alphabetically = list(sorted(map(lambda item: item.name, self.active_countries)))
        self.assertEqual(response_names, active_countries_names_ordered_alphabetically)


@override_settings(ROOT_URLCONF='geo.urls')
class ListRegionsAPITestCase(TestCase):

    def setUp(self):
        self.client = APIClient()

        self.active_countries = [
            Country.objects.create(name="Active Country A", status=Country.STATUS.ACTIVE),
            Country.objects.create(name="Active Country B", status=Country.STATUS.ACTIVE)
        ]
        self.inactive_country = Country.objects.create(name="Inactive Country", status=Country.STATUS.INACTIVE)

        self.active_regions = [
            Region.objects.create(name="Region E", country=self.active_countries[0], status=Region.STATUS.ACTIVE),
            Region.objects.create(name="Region D", country=self.active_countries[1], status=Region.STATUS.ACTIVE)
        ]

        self.inactive_regions = [
            Region.objects.create(name="Region C", country=self.inactive_country, status=Region.STATUS.INACTIVE),
            Region.objects.create(name="Region B active country but inactive status", country=self.active_countries[0], status=Region.STATUS.INACTIVE),
            Region.objects.create(name="Region C active status but inactive country", country=self.inactive_country, status=Region.STATUS.ACTIVE),
        ]

    def test_only_active_regions_are_listed(self):
        response = self.client.get('/1.0/regions/')
        self.assertEqual(len(response.data), len(self.active_regions))

        active_regions_names = list(map(lambda item: item.name, self.active_regions))
        inactive_regions_names = list(map(lambda item: item.name, self.inactive_regions))
        response_names = list(map(lambda item: item.get("name"), response.data))

        for name in response_names:
            self.assertIn(name, active_regions_names)

        for name in response_names:
            self.assertNotIn(name, inactive_regions_names)

    def test_regions_are_listed_alphabetically(self):
        response = self.client.get('/1.0/regions/')
        response_names = list(map(lambda item: item.get("name"), response.data))
        active_regions_names_ordered_alphabetically = list(sorted(map(lambda item: item.name, self.active_regions)))
        self.assertEqual(response_names, active_regions_names_ordered_alphabetically)

    def test_regions_filtered_by_country(self):
        for country in self.active_countries:
            response = self.client.get('/1.0/regions/?country={0}'.format(country.id))
            regions_in_country = Region.objects.filter(country=country, status=Region.STATUS.ACTIVE)
            self.assertEqual(len(response.data), len(regions_in_country))
            response_regions_ids = list(sorted(map(lambda item: item.get("id"), response.data)))
            database_regions_ids = list(sorted(map(lambda item: item.id, regions_in_country)))
            self.assertEqual(response_regions_ids, database_regions_ids)


@override_settings(ROOT_URLCONF='geo.urls')
class ListCitiesAPITestCase(TestCase):

    def setUp(self):
        self.client = APIClient()

        self.active_countries = [
            Country.objects.create(name="Active Country A", status=Country.STATUS.ACTIVE),
            Country.objects.create(name="Active Country B", status=Country.STATUS.ACTIVE)
        ]
        inactive_country = Country.objects.create(name="Inactive Country", status=Country.STATUS.INACTIVE)

        active_region_active_country = Region.objects.create(name="Region AA", country=self.active_countries[0], status=Region.STATUS.ACTIVE)
        active_region_inactive_country = Region.objects.create(name="Region AI", country=inactive_country, status=Region.STATUS.ACTIVE)
        self.active_regions = [active_region_active_country, active_region_inactive_country]
        inactive_region_active_country = Region.objects.create(name="Region IA", country=self.active_countries[1], status=Region.STATUS.INACTIVE)
        inactive_region_inactive_country = Region.objects.create(name="Region II", country=inactive_country, status=Region.STATUS.INACTIVE)

        self.active_cities = [
            City.objects.create(name="City B", region=active_region_active_country, country=self.active_countries[0], status=City.STATUS.ACTIVE),
            City.objects.create(name="City A", region=active_region_active_country, country=self.active_countries[1], status=City.STATUS.ACTIVE)
        ]

        self.inactive_cities = [
            City.objects.create(name="City active in active region but inactive country", region=active_region_inactive_country, country=inactive_country, status=City.STATUS.ACTIVE),
            City.objects.create(name="City active in inactive region but active country", region=inactive_region_active_country, country=self.active_countries[0], status=City.STATUS.ACTIVE),
            City.objects.create(name="City active in inactive region in inactive country", region=inactive_region_inactive_country, country=inactive_country, status=City.STATUS.ACTIVE),
            City.objects.create(name="City inactive in active region in active country", region=active_region_active_country, country=self.active_countries[1], status=City.STATUS.INACTIVE)
        ]

    def test_only_active_cities_are_listed(self):
        response = self.client.get('/1.0/cities/')
        self.assertEqual(len(response.data), len(self.active_cities))

        active_cities_names = list(map(lambda item: item.name, self.active_cities))
        inactive_cities_names = list(map(lambda item: item.name, self.inactive_cities))
        response_names = list(map(lambda item: item.get("name"), response.data))

        for name in response_names:
            self.assertIn(name, active_cities_names)

        for name in response_names:
            self.assertNotIn(name, inactive_cities_names)

    def test_cities_are_listed_alphabetically(self):
        response = self.client.get('/1.0/cities/')
        response_names = list(map(lambda item: item.get("name"), response.data))
        active_cities_names_ordered_alphabetically = list(sorted(map(lambda item: item.name, self.active_cities)))
        self.assertEqual(response_names, active_cities_names_ordered_alphabetically)

    def test_cities_filtered_by_country(self):
        for country in self.active_countries:
            response = self.client.get('/1.0/cities/?country={0}'.format(country.id))
            cities_in_country = City.objects.filter(country=country, status=City.STATUS.ACTIVE, region__status=Region.STATUS.ACTIVE)
            self.assertEqual(len(response.data), len(cities_in_country))
            response_cities_ids = list(sorted(map(lambda item: item.get("id"), response.data)))
            database_cities_ids = list(sorted(map(lambda item: item.id, cities_in_country)))
            self.assertEqual(response_cities_ids, database_cities_ids)

    def test_cities_filtered_by_region(self):
        for region in self.active_regions:
            response = self.client.get('/1.0/cities/?region={0}'.format(region.id))
            cities_in_region = City.objects.filter(region=region, status=City.STATUS.ACTIVE, country__status=Country.STATUS.ACTIVE)
            self.assertEqual(len(response.data), len(cities_in_region))
            response_cities_ids = list(sorted(map(lambda item: item.get("id"), response.data)))
            database_cities_ids = list(sorted(map(lambda item: item.id, cities_in_region)))
            self.assertEqual(response_cities_ids, database_cities_ids)



@override_settings(ROOT_URLCONF='geo.urls')
class ListWorkZonesAPITestCase(TestCase):

    def setUp(self):
        self.client = APIClient()

        self.active_country = Country.objects.create(name="Active Country A", status=Country.STATUS.ACTIVE)
        self.inactive_country = Country.objects.create(name="Inactive Country", status=Country.STATUS.INACTIVE)

        self.active_region_active_country = Region.objects.create(name="Region AA", country=self.active_country, status=Region.STATUS.ACTIVE)
        self.active_region_inactive_country = Region.objects.create(name="Region AI", country=self.inactive_country, status=Region.STATUS.ACTIVE)
        self.inactive_region = Region.objects.create(name="Region IA", country=self.active_country, status=Region.STATUS.INACTIVE)

        self.active_cities = [
            City.objects.create(name="City A", region=self.active_region_active_country, country=self.active_country, status=City.STATUS.ACTIVE),
            City.objects.create(name="City B", region=self.active_region_active_country, country=self.active_country, status=City.STATUS.ACTIVE)
        ]

        self.inactive_cities = [
            City.objects.create(name="City active in active region but inactive country", region=self.active_region_active_country, country=self.inactive_country, status=City.STATUS.ACTIVE),
            City.objects.create(name="City active in inactive region but active country", region=self.inactive_region, country=self.active_country, status=City.STATUS.ACTIVE),
            City.objects.create(name="City active in inactive region in inactive country", region=self.inactive_region, country=self.inactive_country, status=City.STATUS.ACTIVE),
            City.objects.create(name="City inactive in active region in active country", region=self.active_region_active_country, country=self.active_country, status=City.STATUS.INACTIVE)
        ]

        self.active_workzones = [
            WorkZone.objects.create(name="Active Workzone 1", city=self.active_cities[0], zip_codes=["1", "2"], status=WorkZone.STATUS.ACTIVE),
            WorkZone.objects.create(name="Active Workzone 2", city=self.active_cities[0], zip_codes=["1", "2"], status=WorkZone.STATUS.ACTIVE),
            WorkZone.objects.create(name="Active Workzone 3", city=self.active_cities[0], zip_codes=["1", "2"], status=WorkZone.STATUS.ACTIVE),
            WorkZone.objects.create(name="Active Workzone 4", city=self.active_cities[1], zip_codes=["1", "2"], status=WorkZone.STATUS.ACTIVE),
            WorkZone.objects.create(name="Active Workzone 5", city=self.active_cities[1], zip_codes=["1", "2"], status=WorkZone.STATUS.ACTIVE),
        ]

        self.inactive_workzones = [WorkZone.objects.create(name="Inactive Workzone", city=self.active_cities[0], zip_codes=["1", "2"], status=WorkZone.STATUS.INACTIVE)]
        for city in self.inactive_cities:
            self.inactive_workzones.append(
                WorkZone.objects.create(name="Inactive City Workzone", city=city, zip_codes=["1", "2"], status=WorkZone.STATUS.ACTIVE),
            )

    def test_only_active_workzones_are_listed(self):
        response = self.client.get('/1.0/zones/')
        self.assertEqual(len(response.data), len(self.active_workzones))

        active_workzones_names = list(map(lambda item: item.name, self.active_workzones))
        inactive_workzones_names = list(map(lambda item: item.name, self.inactive_workzones))
        response_names = list(map(lambda item: item.get("name"), response.data))

        for name in response_names:
            self.assertIn(name, active_workzones_names)

        for name in response_names:
            self.assertNotIn(name, inactive_workzones_names)


    def test_workzones_are_listed_alphabetically(self):
        response = self.client.get('/1.0/zones/')
        response_names = list(map(lambda item: item.get("name"), response.data))
        active_workzones_names_ordered_alphabetically = list(sorted(map(lambda item: item.name, self.active_workzones)))
        self.assertEqual(response_names, active_workzones_names_ordered_alphabetically)


    def test_workzones_filtered_by_city(self):
        for city in self.active_cities:
            response = self.client.get('/1.0/zones/?city={0}'.format(city.id))
            zones_in_city = WorkZone.objects.filter(
                city=city,
                status=WorkZone.STATUS.ACTIVE,
                city__region__status=Region.STATUS.ACTIVE,
                city__country__status=Country.STATUS.ACTIVE
            )
            self.assertEqual(len(response.data), len(zones_in_city))
            response_zones_ids = list(sorted(map(lambda item: item.get("id"), response.data)))
            database_zones_ids = list(sorted(map(lambda item: item.id, zones_in_city)))
            self.assertEqual(response_zones_ids, database_zones_ids)
