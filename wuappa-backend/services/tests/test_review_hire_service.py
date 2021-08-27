# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from django.test import TestCase, override_settings
from django.utils.translation import ugettext_lazy as _
from rest_auth.utils import jwt_encode
from rest_framework import status
from rest_framework.test import APIClient

from services.models import HireService
from services.settings import COMPLETE


@override_settings(ROOT_URLCONF='services.urls')
class TestClientReviewHireServiceAPI(TestCase):
    fixtures = ['registration_fixtures.json', 'hireservice_test.json']

    def setUp(self):
        self.superuser = User.objects.get(pk=1)
        self.professional = User.objects.get(pk=3)
        self.final = User.objects.get(pk=4)
        self.final_2 = User.objects.get(pk=2)
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

    def test_review_hire_service_client_ok(self):
        final = self.final
        token_jwt_1 = jwt_encode(final)

        self.hire_service_4.status = COMPLETE
        self.hire_service_4.save()

        data = {
            "id": self.hire_service_4.pk,
            "rating": 4,
            "review": "Servicio OK"
        }

        client = APIClient()
        response = client.put("/1.0/hire-services/", data=data, format='json',
                              HTTP_AUTHORIZATION='Token {}'.format(token_jwt_1))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_review_hire_service_user_not_final(self):
        professional = self.professional
        token_jwt_1 = jwt_encode(professional)

        self.hire_service_4.status = COMPLETE
        self.hire_service_4.save()

        data = {
            "id": self.hire_service_4.pk,
            "rating": 4,
            "review": "Servicio OK"
        }

        client = APIClient()
        response = client.put("/1.0/hire-services/", data=data, format='json',
                              HTTP_AUTHORIZATION='Token {}'.format(token_jwt_1))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data.get('non_field_errors')[0], _("User must be a final."))

    def test_review_hire_service_status_is_not_complete(self):
        final = self.final
        token_jwt_1 = jwt_encode(final)

        data = {
            "id": self.hire_service_4.pk,
            "rating": 4,
            "review": "Servicio OK"
        }

        client = APIClient()
        response = client.put("/1.0/hire-services/", data=data, format='json',
                              HTTP_AUTHORIZATION='Token {}'.format(token_jwt_1))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data.get('id')[0], _("Invalid pk \"4\" - object does not exist."))

    def test_review_hire_service_invalid_rating_value(self):
        final = self.final
        token_jwt_1 = jwt_encode(final)

        self.hire_service_4.status = COMPLETE
        self.hire_service_4.save()

        data = {
            "id": self.hire_service_4.pk,
            "rating": 6,
            "review": "Servicio OK"
        }

        client = APIClient()
        response = client.put("/1.0/hire-services/", data=data, format='json',
                              HTTP_AUTHORIZATION='Token {}'.format(token_jwt_1))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data.get('rating')[0], _("Ensure this value is less than or equal to 5."))

    def test_review_hire_service_review_sent_blank(self):
        final = self.final
        token_jwt_1 = jwt_encode(final)

        self.hire_service_4.status = COMPLETE
        self.hire_service_4.save()

        data = {
            "id": self.hire_service_4.pk,
            "rating": 4,
            "review": ""
        }

        client = APIClient()
        response = client.put("/1.0/hire-services/", data=data, format='json',
                              HTTP_AUTHORIZATION='Token {}'.format(token_jwt_1))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data.get('review')[0], _("This field may not be blank."))

    def test_review_hire_service_belongs_to_another_user(self):
        final_2 = self.final_2
        token_jwt_1 = jwt_encode(final_2)

        self.hire_service_4.status = COMPLETE
        self.hire_service_4.save()

        data = {
            "id": self.hire_service_4.pk,
            "rating": 4,
            "review": "Servicio OK"
        }

        client = APIClient()
        response = client.put("/1.0/hire-services/", data=data, format='json',
                              HTTP_AUTHORIZATION='Token {}'.format(token_jwt_1))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data.get('non_field_errors')[0],
                         _("Only client for the hire services can review the service."))

    def test_review_hire_service_id_not_sent(self):
        final = self.final
        token_jwt_1 = jwt_encode(final)

        self.hire_service_4.status = COMPLETE
        self.hire_service_4.save()

        data = {
            "rating": 4,
            "review": "Servicio OK"
        }

        client = APIClient()
        response = client.put("/1.0/hire-services/", data=data, format='json',
                              HTTP_AUTHORIZATION='Token {}'.format(token_jwt_1))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_review_hire_service_rating_not_sent(self):
        professional = self.professional
        token_jwt_1 = jwt_encode(professional)

        self.hire_service_4.status = COMPLETE
        self.hire_service_4.save()

        data = {
            "id": self.hire_service_4.pk,
            "review": "Servicio OK"
        }

        client = APIClient()
        response = client.put("/1.0/hire-services/", data=data, format='json',
                              HTTP_AUTHORIZATION='Token {}'.format(token_jwt_1))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_review_hire_service_review_not_sent(self):
        professional = self.professional
        token_jwt_1 = jwt_encode(professional)

        self.hire_service_4.status = COMPLETE
        self.hire_service_4.save()

        data = {
            "id": self.hire_service_4.pk,
            "rating": 4
        }

        client = APIClient()
        response = client.put("/1.0/hire-services/", data=data, format='json',
                              HTTP_AUTHORIZATION='Token {}'.format(token_jwt_1))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
