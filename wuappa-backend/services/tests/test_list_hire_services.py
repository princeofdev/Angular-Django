# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from django.test import TestCase, override_settings
from rest_auth.utils import jwt_encode
from rest_framework import status
from rest_framework.test import APIClient

from services.models import UserService


@override_settings(ROOT_URLCONF='services.urls')
class TestListHireServiceAPI(TestCase):
    fixtures = ['registration_fixtures.json', 'hireservice_test.json']

    def setUp(self):
        self.superuser = User.objects.get(pk=1)
        self.professional = User.objects.get(pk=3)
        self.final = User.objects.get(pk=4)
        self.final_2 = User.objects.get(pk=2)

    def test_user_is_not_authenticate(self):
        client = APIClient()
        response = client.get("/1.0/hire-services/", format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_user_is_superuser(self):
        superuser = self.superuser
        token_jwt_1 = jwt_encode(superuser)

        client = APIClient()
        response = client.get("/1.0/hire-services/", format='json', HTTP_AUTHORIZATION='Token {}'.format(token_jwt_1))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()
        self.assertEqual(len(data), 5)

    def test_user_is_final(self):
        final = self.final
        token_jwt_1 = jwt_encode(final)

        client = APIClient()
        response = client.get("/1.0/hire-services/", format='json', HTTP_AUTHORIZATION='Token {}'.format(token_jwt_1))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()
        self.assertEqual(len(data), 3)

    def test_user_is_professional(self):
        professional = self.professional
        token_jwt_1 = jwt_encode(professional)

        client = APIClient()
        response = client.get("/1.0/hire-services/", format='json', HTTP_AUTHORIZATION='Token {}'.format(token_jwt_1))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()
        self.assertEqual(len(data), 3)

    def test_user_is_professional_and_has_services_refused(self):
        professional = self.professional
        token_jwt_1 = jwt_encode(professional)

        client = APIClient()
        response = client.get("/1.0/hire-services/", format='json', HTTP_AUTHORIZATION='Token {}'.format(token_jwt_1))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertEqual(len(data), 3)

        response = client.delete(
            "/1.0/hire-services/4/", data={}, format='json', HTTP_AUTHORIZATION='Token {}'.format(token_jwt_1)
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        response = client.get("/1.0/hire-services/", format='json', HTTP_AUTHORIZATION='Token {}'.format(token_jwt_1))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertEqual(len(data), 2)

    def test_user_is_professional_without_user_services(self):
        professional = self.professional
        token_jwt_1 = jwt_encode(professional)

        UserService.objects.filter(user=professional).delete()

        client = APIClient()
        response = client.get("/1.0/hire-services/", format='json', HTTP_AUTHORIZATION='Token {}'.format(token_jwt_1))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()
        self.assertEqual(len(data), 2)

    def test_user_is_final_filter_by_status(self):
        final = self.final
        token_jwt_1 = jwt_encode(final)

        client = APIClient()
        response = client.get("/1.0/hire-services/?status=PEN", format='json',
                              HTTP_AUTHORIZATION='Token {}'.format(token_jwt_1))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()
        self.assertEqual(len(data), 2)

    def test_user_is_final_filter_by_review(self):
        final_2 = self.final_2
        token_jwt_1 = jwt_encode(final_2)

        self.final_2.is_superuser = False
        self.final_2.save()

        client = APIClient()
        response = client.get("/1.0/hire-services/?review=true", format='json',
                              HTTP_AUTHORIZATION='Token {}'.format(token_jwt_1))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()
        self.assertEqual(len(data), 1)

    def test_user_is_professional_filter_by_status(self):
        professional = self.professional
        token_jwt_1 = jwt_encode(professional)

        client = APIClient()
        response = client.get("/1.0/hire-services/?status=ACP", format='json',
                              HTTP_AUTHORIZATION='Token {}'.format(token_jwt_1))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()
        self.assertEqual(len(data), 1)
