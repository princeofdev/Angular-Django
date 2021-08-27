# -*- coding: utf-8 -*-
from copy import deepcopy

from django.contrib.auth.models import User
from django.test import TestCase, override_settings
from django.utils.translation import ugettext_lazy as _
from djstripe.models import Card
from rest_auth.utils import jwt_encode
from rest_framework import status
from rest_framework.test import APIClient

from services.models import HireService
from . import FAKE_CUSTOMER, FAKE_CARD


@override_settings(ROOT_URLCONF='services.urls')
class TestProfessionalCompleteHireServiceAPI(TestCase):
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

        # Add credit card to user_final
        self.customer = FAKE_CUSTOMER.create_for_user(self.final)
        Card.sync_from_stripe_data(deepcopy(FAKE_CARD))

        # Add credit card for hire service
        self.hire_service_2.credit_card = FAKE_CARD['id']
        self.hire_service_2.save()

    def test_user_is_not_authenticate(self):
        data = {
            "complete": True,
            "id": self.hire_service_2.pk
        }

        client = APIClient()
        response = client.put("/1.0/hire-services/", data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # def test_complete_hire_service_professional__ok(self):
    #     professional = self.professional
    #     token_jwt_1 = jwt_encode(professional)
    #
    #     data = {
    #         "complete": True,
    #         "id": self.hire_service_2.pk
    #     }
    #
    #     client = APIClient()
    #     self.assertEqual(Charge.objects.all().count(), 0)
    #     response = client.put("/1.0/hire-services/", data=data, format='json',
    #                           HTTP_AUTHORIZATION='Token {}'.format(token_jwt_1))
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     self.assertEqual(HireService.objects.get(pk=1).status, COMPLETE)
    #     self.assertEqual(Charge.objects.all().count(), 1)

    def test_complete_hire_service_user_not_professional(self):
        final = self.final
        token_jwt_1 = jwt_encode(final)

        data = {
            "complete": True,
            "id": self.hire_service_2.pk
        }

        client = APIClient()
        response = client.put("/1.0/hire-services/", data=data, format='json',
                              HTTP_AUTHORIZATION='Token {}'.format(token_jwt_1))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data.get('non_field_errors')[0], _("User must be a professional."))

    def test_complete_hire_service_status_is_not_accept(self):
        professional = self.professional
        token_jwt_1 = jwt_encode(professional)

        data = {
            "complete": True,
            "id": self.hire_service_4.pk
        }

        client = APIClient()
        response = client.put("/1.0/hire-services/", data=data, format='json',
                              HTTP_AUTHORIZATION='Token {}'.format(token_jwt_1))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data.get('id')[0], _("Invalid pk \"4\" - object does not exist."))

    def test_complete_hire_service_belongs_to_another_user(self):
        professional = self.professional_2
        token_jwt_1 = jwt_encode(professional)

        data = {
            "complete": True,
            "id": self.hire_service_2.pk
        }

        client = APIClient()
        response = client.put("/1.0/hire-services/", data=data, format='json',
                              HTTP_AUTHORIZATION='Token {}'.format(token_jwt_1))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data.get('non_field_errors')[0],
                         _("Only professional for the hire services can complete the service."))

    def test_complete_hire_service_id_not_sent(self):
        professional = self.professional
        token_jwt_1 = jwt_encode(professional)

        data = {
            "complete": True
        }

        client = APIClient()
        response = client.put("/1.0/hire-services/", data=data, format='json',
                              HTTP_AUTHORIZATION='Token {}'.format(token_jwt_1))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_complete_hire_service_complete_not_sent(self):
        professional = self.professional
        token_jwt_1 = jwt_encode(professional)

        data = {
            "id": self.hire_service_2.pk
        }

        client = APIClient()
        response = client.put("/1.0/hire-services/", data=data, format='json',
                              HTTP_AUTHORIZATION='Token {}'.format(token_jwt_1))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
