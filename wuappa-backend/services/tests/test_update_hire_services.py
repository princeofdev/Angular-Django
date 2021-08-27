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
from . import FAKE_CUSTOMER, FAKE_CARD, FAKE_CUSTOMER_II, FAKE_CARD_II


@override_settings(ROOT_URLCONF='services.urls')
class TestUpdateHireServiceAPI(TestCase):
    fixtures = ['registration_fixtures.json', 'hireservice_test.json']

    def setUp(self):
        self.superuser = User.objects.get(pk=1)
        self.professional = User.objects.get(pk=3)
        self.final = User.objects.get(pk=4)

        self.hire_service_1 = HireService.objects.get(pk=1)
        self.hire_service_2 = HireService.objects.get(pk=2)

    def test_user_is_not_authenticate(self):
        data = {
            "professional": self.professional.pk
        }

        client = APIClient()
        response = client.patch("/1.0/hire-services/", data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_hire_service_final__ok(self):
        final = self.final
        token_jwt_1 = jwt_encode(final)
        self.customer = FAKE_CUSTOMER.create_for_user(self.final)
        Card.sync_from_stripe_data(deepcopy(FAKE_CARD))

        data = {
            "credit_card": FAKE_CARD['id']
        }

        client = APIClient()
        response = client.patch("/1.0/hire-services/{0}/".format(self.hire_service_1.pk), data=data, format='json',
                                HTTP_AUTHORIZATION='Token {}'.format(token_jwt_1))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(HireService.objects.get(pk=1).credit_card, FAKE_CARD['id'])

    def test_update_hire_service_professional__ko(self):
        professional = self.professional
        token_jwt_1 = jwt_encode(professional)
        self.customer = FAKE_CUSTOMER.create_for_user(self.final)
        Card.sync_from_stripe_data(deepcopy(FAKE_CARD))

        data = {
            "credit_card": FAKE_CARD['id']
        }

        client = APIClient()
        response = client.patch("/1.0/hire-services/{0}/".format(self.hire_service_1.pk), data=data, format='json',
                                HTTP_AUTHORIZATION='Token {}'.format(token_jwt_1))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data.get('non_field_errors')[0], _("Only client for the hire services can update credit card"))

    def test_update_hire_service_final_ko_credit_card_not_belongs_to_client(self):
        final = self.final
        token_jwt_1 = jwt_encode(final)
        self.customer = FAKE_CUSTOMER.create_for_user(self.final)
        Card.sync_from_stripe_data(deepcopy(FAKE_CARD))

        self.customer_2 = FAKE_CUSTOMER_II.create_for_user(self.professional)
        Card.sync_from_stripe_data(deepcopy(FAKE_CARD_II))

        data = {
            "credit_card": FAKE_CARD_II['id']
        }

        client = APIClient()
        response = client.patch("/1.0/hire-services/{0}/".format(self.hire_service_1.pk), data=data, format='json',
                                HTTP_AUTHORIZATION='Token {}'.format(token_jwt_1))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data.get('non_field_errors')[0], _("Credit card number not belongs to the client"))

    def test_update_hire_service_not_exist_ko(self):
        final = self.final
        token_jwt_1 = jwt_encode(final)
        self.customer = FAKE_CUSTOMER.create_for_user(self.final)
        Card.sync_from_stripe_data(deepcopy(FAKE_CARD))

        data = {
             "credit_card": FAKE_CARD_II['id']
        }

        client = APIClient()
        response = client.patch("/1.0/hire-services/0/", data=data, format='json',
                                HTTP_AUTHORIZATION='Token {}'.format(token_jwt_1))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_hire_service_final_ko_credit_card_sent_null(self):
        final = self.final
        token_jwt_1 = jwt_encode(final)
        self.customer = FAKE_CUSTOMER.create_for_user(self.final)
        Card.sync_from_stripe_data(deepcopy(FAKE_CARD))

        data = {
            "credit_card": ""
        }

        client = APIClient()
        response = client.patch("/1.0/hire-services/{0}/".format(self.hire_service_1.pk), data=data, format='json',
                                HTTP_AUTHORIZATION='Token {}'.format(token_jwt_1))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data.get('credit_card')[0], _("This field may not be blank."))

    def test_update_hire_service_final_ko_credit_card_invalid(self):
        final = self.final
        token_jwt_1 = jwt_encode(final)
        self.customer = FAKE_CUSTOMER.create_for_user(self.final)
        Card.sync_from_stripe_data(deepcopy(FAKE_CARD))

        data = {
            "credit_card": "aaaaaaa"
        }

        client = APIClient()
        response = client.patch("/1.0/hire-services/{0}/".format(self.hire_service_1.pk), data=data, format='json',
                                HTTP_AUTHORIZATION='Token {}'.format(token_jwt_1))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data.get('credit_card')[0], _("Credit card id is not included in app."))
