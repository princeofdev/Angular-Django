from django.contrib.auth.models import User
from django.test import TestCase, override_settings
from rest_framework.test import APIClient

from geo.models import City, Country, WorkZone
from services.models import Category, Service, CityServices
from services.settings import ACTIVE, PUBLIC, INACTIVE, PRIVATE


@override_settings(ROOT_URLCONF='services.urls')
class ListCategoriesAPITestCase(TestCase):

    def setUp(self):
        self.client = APIClient()

        self.public_active_categories = [
            Category.objects.create(name="Public Active 1", type=PUBLIC, status=ACTIVE),
            Category.objects.create(name="Public Active 2", type=PUBLIC, status=ACTIVE)
        ]

        self.active_categories = self.public_active_categories + [
            Category.objects.create(name="Private Active 1", type=PRIVATE, status=ACTIVE),
            Category.objects.create(name="Private Active 2", type=PRIVATE, status=ACTIVE)
        ]

        Category.objects.create(name="Public Inactive", type=PUBLIC, status=INACTIVE)
        Category.objects.create(name="Private Inactive", type=PRIVATE, status=INACTIVE)

    def test_only_public_active_categories_are_listed_when_not_authenticated(self):
        response = self.client.get('/1.0/categories/')
        self.assertEqual(len(response.data), len(self.public_active_categories))
        categories_names = list(map(lambda item: item.name, self.public_active_categories))
        response_names = list(map(lambda item: item.get("name"), response.data))
        for name in response_names:
            self.assertIn(name, categories_names)

    def test_all_active_categories_are_list_when_authenticated(self):
        user = User.objects.create_user("username", "user@user.com", "password")
        self.client.force_authenticate(user=user)
        response = self.client.get('/1.0/categories/')
        self.assertEqual(len(response.data), len(self.active_categories))
        categories_names = list(map(lambda item: item.name, self.active_categories))
        response_names = list(map(lambda item: item.get("name"), response.data))
        for name in response_names:
            self.assertIn(name, categories_names)


@override_settings(ROOT_URLCONF='services.urls')
class ListServicesAPITestCase(TestCase):

    def setUp(self):
        self.client = APIClient()

        self.user = User.objects.create_user("username", "user@user.com", "password")

        self.public_active_category = Category.objects.create(name="Public Active 1", type=PUBLIC, status=ACTIVE)
        self.private_active_category = Category.objects.create(name="Private Active 1", type=PRIVATE, status=ACTIVE)

        self.public_active_services = [
            Service.objects.create(
                name="Public Active Public Category 1", category=self.public_active_category, type=PUBLIC, status=ACTIVE
            ),
            Service.objects.create(
                name="Public Active Public Category 2", category=self.public_active_category, type=PUBLIC, status=ACTIVE
            )
        ]

        self.active_services = self.public_active_services + [
            Service.objects.create(
                name="Private Active Public Category", category=self.public_active_category, type=PRIVATE, status=ACTIVE
            ),
            Service.objects.create(
                name="Public Active Private Category", category=self.private_active_category, type=PUBLIC, status=ACTIVE
            ),
            Service.objects.create(
                name="Private Active Private Category", category=self.private_active_category, type=PRIVATE, status=ACTIVE
            )
        ]

        public_inactive_category = Category.objects.create(name="Public Inactive", type=PUBLIC, status=INACTIVE)
        private_inactive_category = Category.objects.create(name="Private Inactive", type=PRIVATE, status=INACTIVE)

        Service.objects.create(
            name="Public Active in Inactive Category", category=public_inactive_category, type=PUBLIC, status=ACTIVE
        )
        Service.objects.create(
            name="Public Active in Inactive Category", category=private_inactive_category, type=PUBLIC, status=ACTIVE
        )
        Service.objects.create(
            name="Public Inactive in Public Category", category=public_inactive_category, type=PUBLIC, status=INACTIVE
        )
        Service.objects.create(
            name="Public Inactive in Private Category", category=private_inactive_category, type=PUBLIC, status=INACTIVE
        )

    def test_only_public_active_services_are_listed_when_not_authenticated(self):
        response = self.client.get('/1.0/services/')
        self.assertEqual(len(response.data), len(self.public_active_services))
        services_names = list(map(lambda item: item.name, self.public_active_services))
        response_names = list(map(lambda item: item.get("name"), response.data))
        for name in response_names:
            self.assertIn(name, services_names)

    def test_all_active_services_are_list_when_authenticated(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get('/1.0/services/')
        self.assertEqual(len(response.data), len(self.active_services))
        services_names = list(map(lambda item: item.name, self.active_services))
        response_names = list(map(lambda item: item.get("name"), response.data))
        for name in response_names:
            self.assertIn(name, services_names)


@override_settings(ROOT_URLCONF='services.urls')
class FilterServicesCategoriesByCityAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

        # Cities
        country = Country.objects.create(name="Active Country", status=Country.STATUS.ACTIVE)
        self.citi_a = City.objects.create(name="City A", country=country)
        self.citi_b = City.objects.create(name="City B", country=country)

        # Categories
        self.category_a = Category.objects.create(name="Category A", type=PUBLIC, status=ACTIVE)
        self.category_b = Category.objects.create(name="Category B", type=PUBLIC, status=ACTIVE)

        # Services
        self.city_a_services = [
            Service.objects.create(name="Public Active 1", category=self.category_a, type=PUBLIC, status=ACTIVE),
            Service.objects.create(name="Public Active 2", category=self.category_a, type=PUBLIC, status=ACTIVE),
            Service.objects.create(name="Public Active 3", category=self.category_a, type=PUBLIC, status=ACTIVE)
        ]
        for service in self.city_a_services:
            CityServices.objects.create(city=self.citi_a, service=service)

        self.city_b_services = [
            Service.objects.create(name="Public Active 3", category=self.category_b, type=PUBLIC, status=ACTIVE),
            Service.objects.create(name="Public Active 4", category=self.category_b, type=PUBLIC, status=ACTIVE)
        ]
        for service in self.city_b_services:
            CityServices.objects.create(city=self.citi_b, service=service)

        both_cities_services = [
            Service.objects.create(name="Public Active 5", category=self.category_a, type=PUBLIC, status=ACTIVE),
            Service.objects.create(name="Public Active 6", category=self.category_b, type=PUBLIC, status=ACTIVE)
        ]
        for service in both_cities_services:
            CityServices.objects.create(city=self.citi_a, service=service)
            CityServices.objects.create(city=self.citi_b, service=service)

        self.city_a_services += both_cities_services
        self.city_b_services += both_cities_services

    def test_filter_services_by_city(self):
        response = self.client.get('/1.0/services/?cities={0}'.format(self.citi_a.pk))
        self.assertEqual(len(response.data), len(self.city_a_services))
        services_names = list(map(lambda item: item.name, self.city_a_services))
        response_names = list(map(lambda item: item.get("name"), response.data))
        for name in response_names:
            self.assertIn(name, services_names)

        response = self.client.get('/1.0/services/?cities={0}'.format(self.citi_b.pk))
        self.assertEqual(len(response.data), len(self.city_b_services))
        services_names = list(map(lambda item: item.name, self.city_b_services))
        response_names = list(map(lambda item: item.get("name"), response.data))
        for name in response_names:
            self.assertIn(name, services_names)

    def test_filter_categories_by_city(self):
        response = self.client.get('/1.0/categories/?cities={0}'.format(self.citi_a.pk))
        self.assertEqual(len(response.data), 2)

        response = self.client.get('/1.0/categories/?cities={0}'.format(self.citi_b.pk))
        self.assertEqual(len(response.data), 2)


@override_settings(ROOT_URLCONF='services.urls')
class FilterServicesCategoriesByZipCodeAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

        # Cities
        country = Country.objects.create(name="Active Country", status=Country.STATUS.ACTIVE)
        self.citi_a = City.objects.create(name="City A", country=country)
        self.citi_b = City.objects.create(name="City B", country=country)
        WorkZone.objects.create(pk=1, city=self.citi_a, name="Zone 1", zip_codes=["28039", "28029"], status="PUB")
        WorkZone.objects.create(pk=2, city=self.citi_b, name="Zone 2", zip_codes=["28029"], status=ACTIVE)
        WorkZone.objects.create(pk=3, city=self.citi_b, name="Zone 3", zip_codes=["08080"], status=ACTIVE)

        # Categories
        self.category_a = Category.objects.create(name="Category A", type=PUBLIC, status=ACTIVE)

        self.category_b = Category.objects.create(name="Category B", type=PUBLIC, status=ACTIVE)

        # Services
        self.city_a_services = [
            Service.objects.create(name="Public Active 1", category=self.category_a, type=PUBLIC, status=ACTIVE),
            Service.objects.create(name="Public Active 2", category=self.category_a, type=PUBLIC, status=ACTIVE),
            Service.objects.create(name="Public Active 3", category=self.category_a, type=PUBLIC, status=ACTIVE)
        ]
        for service in self.city_a_services:
            CityServices.objects.create(city=self.citi_a, service=service)

        self.city_b_services = [
            Service.objects.create(name="Public Active 3", category=self.category_b, type=PUBLIC, status=ACTIVE),
            Service.objects.create(name="Public Active 4", category=self.category_b, type=PUBLIC, status=ACTIVE)
        ]
        for service in self.city_b_services:
            CityServices.objects.create(city=self.citi_b, service=service)

        both_cities_services = [
            Service.objects.create(name="Public Active 5", category=self.category_a, type=PUBLIC, status=ACTIVE),
            Service.objects.create(name="Public Active 6", category=self.category_b, type=PUBLIC, status=ACTIVE)
        ]
        for service in both_cities_services:
            CityServices.objects.create(city=self.citi_a, service=service)
            CityServices.objects.create(city=self.citi_b, service=service)

        self.city_a_services += both_cities_services
        self.city_b_services += both_cities_services

    def test_filter_services_by_zip_code(self):
        response = self.client.get('/1.0/services/?zip={0}'.format("28039"))
        self.assertEqual(len(response.data), len(self.city_a_services))
        services_names = list(map(lambda item: item.name, self.city_a_services))
        response_names = list(map(lambda item: item.get("name"), response.data))
        for name in response_names:
            self.assertIn(name, services_names)

        response = self.client.get('/1.0/services/?zip={0}'.format("08080"))
        self.assertEqual(len(response.data), len(self.city_b_services))
        services_names = list(map(lambda item: item.name, self.city_b_services))
        response_names = list(map(lambda item: item.get("name"), response.data))
        for name in response_names:
            self.assertIn(name, services_names)

    def test_filter_categories_by_zip_code(self):
        response = self.client.get('/1.0/categories/?zip={0}'.format("28039"))
        self.assertEqual(len(response.data), 2)

        response = self.client.get('/1.0/categories/?zip={0}'.format("08080"))
        self.assertEqual(len(response.data), 2)


@override_settings(ROOT_URLCONF='services.urls')
class FilterServicesByWorkZoneAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

        # Cities
        country = Country.objects.create(name="Active Country", status=Country.STATUS.ACTIVE)
        self.citi_a = City.objects.create(name="City A", country=country)
        self.citi_b = City.objects.create(name="City B", country=country)
        self.work_zone_1 = WorkZone.objects.create(pk=1, city=self.citi_a, name="Zone 1", zip_codes=["28039", "28029"], status="PUB")
        self.work_zone_2 = WorkZone.objects.create(pk=2, city=self.citi_b, name="Zone 2", zip_codes=["28029"], status=ACTIVE)
        self.work_zone_3 = WorkZone.objects.create(pk=3, city=self.citi_b, name="Zone 3", zip_codes=["08080"], status=ACTIVE)

        # Categories
        self.category_a = Category.objects.create(name="Category A", type=PUBLIC, status=ACTIVE)

        self.category_b = Category.objects.create(name="Category B", type=PUBLIC, status=ACTIVE)

        # Services
        self.city_a_services = [
            Service.objects.create(name="Public Active 1", category=self.category_a, type=PUBLIC, status=ACTIVE),
            Service.objects.create(name="Public Active 2", category=self.category_a, type=PUBLIC, status=ACTIVE),
            Service.objects.create(name="Public Active 3", category=self.category_a, type=PUBLIC, status=ACTIVE)
        ]
        for service in self.city_a_services:
            CityServices.objects.create(city=self.citi_a, service=service)

        self.city_b_services = [
            Service.objects.create(name="Public Active 3", category=self.category_b, type=PUBLIC, status=ACTIVE),
            Service.objects.create(name="Public Active 4", category=self.category_b, type=PUBLIC, status=ACTIVE)
        ]
        for service in self.city_b_services:
            CityServices.objects.create(city=self.citi_b, service=service)

        both_cities_services = [
            Service.objects.create(name="Public Active 5", category=self.category_a, type=PUBLIC, status=ACTIVE),
            Service.objects.create(name="Public Active 6", category=self.category_b, type=PUBLIC, status=ACTIVE)
        ]
        for service in both_cities_services:
            CityServices.objects.create(city=self.citi_a, service=service)
            CityServices.objects.create(city=self.citi_b, service=service)

        self.city_a_services += both_cities_services
        self.city_b_services += both_cities_services

    def test_filter_services_by_workzone(self):
        response = self.client.get('/1.0/services/?work_zones={0}'.format(self.work_zone_1.pk))
        self.assertEqual(len(response.data), len(self.city_a_services))

        some_zones = str(self.work_zone_1.pk) + ", " + str(self.work_zone_2.pk)
        response = self.client.get('/1.0/services/?work_zones={0}'.format(some_zones))
        self.assertEqual(len(response.data), 7)


@override_settings(ROOT_URLCONF='services.urls')
class FilterServicesByCategoryAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

        # Categories
        self.category_a = Category.objects.create(name="Category A", type=PUBLIC, status=ACTIVE)
        self.category_b = Category.objects.create(name="Category B", type=PUBLIC, status=ACTIVE)

        # Services
        self.category_a_services = [
            Service.objects.create(name="Public Active 1", category=self.category_a, type=PUBLIC, status=ACTIVE),
            Service.objects.create(name="Public Active 2", category=self.category_a, type=PUBLIC, status=ACTIVE),
            Service.objects.create(name="Public Active 3", category=self.category_a, type=PUBLIC, status=ACTIVE)
        ]

        self.category_b_services = [
            Service.objects.create(name="Public Active 3", category=self.category_b, type=PUBLIC, status=ACTIVE),
            Service.objects.create(name="Public Active 4", category=self.category_b, type=PUBLIC, status=ACTIVE)
        ]

    def test_filter_services_by_category(self):
        response = self.client.get('/1.0/services/?category={0}'.format(self.category_a.pk))
        self.assertEqual(len(response.data), len(self.category_a_services))
        services_names = list(map(lambda item: item.name, self.category_a_services))
        response_names = list(map(lambda item: item.get("name"), response.data))
        for name in response_names:
            self.assertIn(name, services_names)

        response = self.client.get('/1.0/services/?category={0}'.format(self.category_b.pk))
        self.assertEqual(len(response.data), len(self.category_b_services))
        services_names = list(map(lambda item: item.name, self.category_b_services))
        response_names = list(map(lambda item: item.get("name"), response.data))
        for name in response_names:
            self.assertIn(name, services_names)
