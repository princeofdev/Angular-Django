# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from django.test import TestCase, override_settings
from django.utils.translation import ugettext_lazy as _
from rest_auth.utils import jwt_encode
from rest_framework import status
from rest_framework.test import APIClient

from services.models import HireService


@override_settings(ROOT_URLCONF='services.urls')
class TestProfessionalAcceptHireServiceAPI(TestCase):
    fixtures = ['registration_fixtures.json', 'hireservice_test.json']

    def setUp(self):
        self.superuser = User.objects.get(pk=1)
        self.professional = User.objects.get(pk=3)
        self.final = User.objects.get(pk=4)
        self.professional_2 = User.objects.get(pk=5)

        self.hire_service_1 = HireService.objects.get(pk=1)
        self.hire_service_2 = HireService.objects.get(pk=2)
        self.hire_service_3 = HireService.objects.get(pk=3)
        self.hire_service_4 = HireService.objects.get(pk=4)

    def test_user_is_not_authenticate(self):
        data = {
            "accept": True,
            "id": self.hire_service_1.pk
        }

        client = APIClient()
        response = client.put("/1.0/hire-services/", data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_accept_hire_service_professional__ok(self):
        professional = self.professional
        token_jwt_1 = jwt_encode(professional)

        data = {
            "accept": True,
            "id": self.hire_service_1.pk
        }

        client = APIClient()
        response = client.put("/1.0/hire-services/", data=data, format='json',
                              HTTP_AUTHORIZATION='Token {}'.format(token_jwt_1))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_accept_hire_service_user_not_professional(self):
        final = self.final
        token_jwt_1 = jwt_encode(final)

        data = {
            "accept": True,
            "id": self.hire_service_1.pk
        }

        client = APIClient()
        response = client.put("/1.0/hire-services/", data=data, format='json',
                              HTTP_AUTHORIZATION='Token {}'.format(token_jwt_1))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data.get('non_field_errors')[0], _("User must be a professional."))

    def test_accept_hire_service_status_is_not_pending(self):
        professional = self.professional_2
        token_jwt_1 = jwt_encode(professional)

        data = {
            "accept": True,
            "id": self.hire_service_2.pk
        }

        client = APIClient()
        response = client.put("/1.0/hire-services/", data=data, format='json',
                              HTTP_AUTHORIZATION='Token {}'.format(token_jwt_1))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data.get('id')[0], _("Invalid pk \"2\" - object does not exist."))

    def test_accept_hire_service_belongs_to_another_user(self):
        professional = self.professional_2
        token_jwt_1 = jwt_encode(professional)

        data = {
            "accept": True,
            "id": self.hire_service_4.pk
        }

        client = APIClient()
        response = client.put("/1.0/hire-services/", data=data, format='json',
                              HTTP_AUTHORIZATION='Token {}'.format(token_jwt_1))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data.get('error'), _("Services has assigned to another professional"))

    def test_accept_hire_service_id_not_sent(self):
        professional = self.professional
        token_jwt_1 = jwt_encode(professional)

        data = {
            "accept": True
        }

        client = APIClient()
        response = client.put("/1.0/hire-services/", data=data, format='json',
                              HTTP_AUTHORIZATION='Token {}'.format(token_jwt_1))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_accept_hire_service_accept_not_sent(self):
        professional = self.professional
        token_jwt_1 = jwt_encode(professional)

        data = {
            "id": self.hire_service_1.pk
        }

        client = APIClient()
        response = client.put("/1.0/hire-services/", data=data, format='json',
                              HTTP_AUTHORIZATION='Token {}'.format(token_jwt_1))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
