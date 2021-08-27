# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from django.test import TestCase, override_settings
from rest_auth.utils import jwt_encode
from rest_framework import status
from rest_framework.test import APIClient

from work_calendars.models import DayOff


@override_settings(ROOT_URLCONF='work_calendars.urls')
class TestListDaysOffAPI(TestCase):
    fixtures = ['registration_fixtures.json', 'hireservice_test.json', 'calendar_test.json']

    def setUp(self):
        self.superuser = User.objects.get(pk=1)
        self.professional = User.objects.get(pk=3)
        self.final = User.objects.get(pk=4)

    def test_user_is_not_authenticate(self):
        client = APIClient()
        response = client.get("/1.0/days-off/", format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_user_is_superuser(self):
        superuser = self.superuser
        token_jwt_1 = jwt_encode(superuser)

        client = APIClient()
        response = client.get("/1.0/days-off/", format='json', HTTP_AUTHORIZATION='Token {}'.format(token_jwt_1))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()
        self.assertEqual(len(data), DayOff.objects.filter(professional=self.superuser).count())

    def test_user_is_professional(self):
        professional = self.professional
        token_jwt_1 = jwt_encode(professional)

        client = APIClient()
        response = client.get("/1.0/days-off/", format='json', HTTP_AUTHORIZATION='Token {}'.format(token_jwt_1))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()
        self.assertEqual(len(data), DayOff.objects.filter(professional=self.professional).count())
