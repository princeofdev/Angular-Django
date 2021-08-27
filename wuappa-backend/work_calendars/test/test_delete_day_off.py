# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from django.test import TestCase, override_settings
from rest_auth.utils import jwt_encode
from rest_framework import status
from rest_framework.test import APIClient

from work_calendars.models import DayOff


@override_settings(ROOT_URLCONF='work_calendars.urls')
class TestDeleteDaysOffAPI(TestCase):
    fixtures = ['registration_fixtures.json', 'hireservice_test.json', 'calendar_test.json']

    def setUp(self):
        self.superuser = User.objects.get(pk=1)
        self.professional = User.objects.get(pk=3)
        self.professional_2 = User.objects.get(pk=5)
        self.final = User.objects.get(pk=4)

        self.day_off_1 = DayOff.objects.get(pk=1)
        self.day_off_2 = DayOff.objects.get(pk=2)
        self.day_off_3 = DayOff.objects.get(pk=5)

        self.days_off_total = DayOff.objects.count()

    def test_user_is_not_authenticate(self):
        client = APIClient()
        response = client.delete("/1.0/days-off/2017-12-07/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_user_is_superuser(self):
        superuser = self.superuser
        token_jwt_1 = jwt_encode(superuser)

        client = APIClient()
        response = client.delete("/1.0/days-off/2017-12-07/", HTTP_AUTHORIZATION='Token {}'.format(token_jwt_1))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(self.days_off_total - 1, DayOff.objects.count())

    def test_user_is_professional(self):
        professional = self.professional
        token_jwt_1 = jwt_encode(professional)

        client = APIClient()
        response = client.delete("/1.0/days-off/2017-12-03/", HTTP_AUTHORIZATION='Token {}'.format(token_jwt_1))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(self.days_off_total - 1, DayOff.objects.count())

    def test_user_is_professional_not_exist_day_off_to_delete(self):
        professional = self.professional_2
        token_jwt_1 = jwt_encode(professional)

        client = APIClient()
        response = client.delete("/1.0/days-off/2017-12-11/", HTTP_AUTHORIZATION='Token {}'.format(token_jwt_1))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_user_is_professional_invalid_date(self):
        professional = self.professional_2
        token_jwt_1 = jwt_encode(professional)

        client = APIClient()
        response = client.delete("/1.0/days-off/11-11-2017/", HTTP_AUTHORIZATION='Token {}'.format(token_jwt_1))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
