# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from django.test import TestCase, override_settings
from rest_auth.utils import jwt_encode
from rest_framework import status
from rest_framework.test import APIClient


@override_settings(ROOT_URLCONF='work_calendars.urls')
class TestCreateDaysOffAPI(TestCase):
    fixtures = ['registration_fixtures.json', 'hireservice_test.json', 'calendar_test.json']

    def setUp(self):
        self.superuser = User.objects.get(pk=1)
        self.professional = User.objects.get(pk=3)
        self.final = User.objects.get(pk=4)

    def test_user_is_not_authenticate(self):
        data = {
            "date": "2018-01-01"
        }
        client = APIClient()
        response = client.post("/1.0/days-off/", data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_user_is_superuser(self):
        superuser = self.superuser
        token_jwt_1 = jwt_encode(superuser)

        data = {
            "date": "2018-01-01"
        }

        client = APIClient()
        response = client.post("/1.0/days-off/", data=data, format='json', HTTP_AUTHORIZATION='Token {}'.format(token_jwt_1))
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_user_is_professional(self):
        professional = self.professional
        token_jwt_1 = jwt_encode(professional)

        data = {
            "date": "2018-01-01"
        }

        client = APIClient()
        response = client.post("/1.0/days-off/",  data=data, format='json', HTTP_AUTHORIZATION='Token {}'.format(token_jwt_1))
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_user_is_professional_sent_another_professional(self):
        professional = self.professional
        token_jwt_1 = jwt_encode(professional)

        data = {
            "pofessional": 1,
            "date": "2018-01-01"
        }

        client = APIClient()
        response = client.post("/1.0/days-off/",  data=data, format='json', HTTP_AUTHORIZATION='Token {}'.format(token_jwt_1))
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_user_is_final(self):
        final = self.final
        token_jwt_1 = jwt_encode(final)

        data = {
            "date": "2018-01-01"
        }

        client = APIClient()
        response = client.post("/1.0/days-off/",  data=data, format='json', HTTP_AUTHORIZATION='Token {}'.format(token_jwt_1))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_is_professional_ko_invalid_date(self):
        professional = self.professional
        token_jwt_1 = jwt_encode(professional)

        data = {
            "date": "01-01-2018"
        }

        client = APIClient()
        response = client.post("/1.0/days-off/",  data=data, format='json', HTTP_AUTHORIZATION='Token {}'.format(token_jwt_1))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_is_professional_date_already_exist(self):
        professional = self.professional
        token_jwt_1 = jwt_encode(professional)

        data = {
            "date": "2017-12-03"
        }

        client = APIClient()
        response = client.post("/1.0/days-off/",  data=data, format='json', HTTP_AUTHORIZATION='Token {}'.format(token_jwt_1))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
