# -*- coding: utf-8 -*-
from datetime import timedelta

from django.contrib.auth.models import User
from django.test import TestCase, override_settings
from django.utils.datetime_safe import datetime, time
from djmoney.money import Money
from rest_framework import status
from rest_framework.test import APIClient

from services.models import HireService
from services.settings import PENDING


@override_settings(ROOT_URLCONF='services.urls')
class TestCancelHireServiceAPI(TestCase):
    fixtures = ['registration_fixtures.json', 'hireservice_test.json']

    def setUp(self):
        self.professional = User.objects.get(pk=3)
        self.final = User.objects.get(pk=4)

        self.hire_service_1 = HireService.objects.create(
            client=self.final,
            professional=self.professional,
            date=datetime.now() + timedelta(days=2),
            time=time(),
            address='address',
            city='city',
            region='region',
            zip_code='zip_code',
            country='country',
            status=PENDING
        )
        self.hire_service_1.total = Money(100, 'EUR')
        self.hire_service_1.save()

        self.hire_service_2 = HireService.objects.create(
            client=self.final,
            professional=self.professional,
            date=datetime.now() + timedelta(hours=13),
            time=datetime.now() + timedelta(hours=13),
            address='address',
            city='city',
            region='region',
            zip_code='zip_code',
            country='country',
            status=PENDING
        )
        self.hire_service_2.total = Money(200, 'EUR')
        self.hire_service_2.save()

        self.hire_service_3 = HireService.objects.create(
            client=self.final,
            professional=self.professional,
            date=datetime.now() + timedelta(hours=11),
            time=datetime.now() + timedelta(hours=11),
            address='address',
            city='city',
            region='region',
            zip_code='zip_code',
            country='country',
            status=PENDING
        )
        self.hire_service_3.total = Money(300, 'EUR')
        self.hire_service_3.save()

    def test_user_is_not_authenticated(self):
        client = APIClient()
        response = client.get("/1.0/hire-services/{0}/cancelability/".format(self.hire_service_1.pk))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_check_cancelable_service(self):
        client = APIClient()
        client.force_authenticate(user=self.final)
        response = client.get("/1.0/hire-services/{0}/cancelability/".format(self.hire_service_1.pk))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('amount'), 0)
        self.assertEqual(response.data.get('currency'), self.hire_service_1.total_currency)

    def test_check_cancelable_service_with_50_percent_charge(self):
        client = APIClient()
        client.force_authenticate(user=self.final)
        response = client.get("/1.0/hire-services/{0}/cancelability/".format(self.hire_service_2.pk))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data.get('amount'), self.hire_service_2.total.amount / 2)
        self.assertEqual(response.data.get('currency'), self.hire_service_2.total_currency)

    def test_check_cancelable_service_with_100_percent_charge(self):
        client = APIClient()
        client.force_authenticate(user=self.final)
        response = client.get("/1.0/hire-services/{0}/cancelability/".format(self.hire_service_3.pk))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data.get('amount'), self.hire_service_3.total.amount)
        self.assertEqual(response.data.get('currency'), self.hire_service_3.total_currency)
