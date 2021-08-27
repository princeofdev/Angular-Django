# -*- coding: utf-8 -*-
from datetime import datetime, timedelta
from django.contrib.auth.models import User
from django.test import TestCase, override_settings
from rest_auth.utils import jwt_encode
from rest_framework import status
from rest_framework.test import APIClient

from services.models import HireService, HireServiceRefuse
from services.settings import COMPLETE, REJECT, CANCEL


@override_settings(ROOT_URLCONF='services.urls')
class TestCancelHireServiceAPI(TestCase):
    fixtures = ['registration_fixtures.json', 'hireservice_test.json']

    def setUp(self):
        self.superuser = User.objects.get(pk=1)
        self.professional = User.objects.get(pk=3)
        self.final = User.objects.get(pk=4)
        self.final_2 = User.objects.get(pk=2)

        self.hire_service_1 = HireService.objects.get(pk=1)
        self.hire_service_2 = HireService.objects.get(pk=2)
        self.hire_service_3 = HireService.objects.get(pk=3)
        self.hire_service_4 = HireService.objects.get(pk=4)

    def test_user_is_not_authenticate(self):
        client = APIClient()
        response = client.delete("/1.0/hire-services/{0}/".format(self.hire_service_1.pk), data={}, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_cancel_hire_service_final_ok_status_pending(self):
        final = self.final
        token_jwt_1 = jwt_encode(final)

        client = APIClient()
        response = client.delete("/1.0/hire-services/{0}/".format(self.hire_service_1.pk), data={}, format='json',
                                 HTTP_AUTHORIZATION='Token {}'.format(token_jwt_1))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_cancel_hire_service_professional_ok_status_accept_date_one_date(self):
        professional = self.professional
        token_jwt_1 = jwt_encode(professional)

        date = datetime.now() + timedelta(days=1)
        self.hire_service_2.date = date
        time = (datetime.now() + timedelta(hours=9)).time()
        self.hire_service_2.time = time
        self.hire_service_2.save()

        client = APIClient()
        response = client.delete("/1.0/hire-services/{0}/".format(self.hire_service_2.pk), data={}, format='json',
                                 HTTP_AUTHORIZATION='Token {}'.format(token_jwt_1))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_cancel_hire_service_professional_can_refuse_service(self):
        professional = self.professional
        token_jwt_1 = jwt_encode(professional)

        refused_services = HireServiceRefuse.objects.filter(
            service=self.hire_service_1, user=self.hire_service_1.professional
        ).count()
        self.assertEqual(0, refused_services)

        client = APIClient()
        response = client.delete("/1.0/hire-services/{0}/".format(self.hire_service_1.pk), data={}, format='json',
                                 HTTP_AUTHORIZATION='Token {}'.format(token_jwt_1))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        refused_services = HireServiceRefuse.objects.filter(service=self.hire_service_1, user=self.professional).count()
        self.assertEqual(1, refused_services)

    def test_cancel_hire_service_professional_ko_status_complete(self):
        professional = self.professional
        token_jwt_1 = jwt_encode(professional)

        self.hire_service_2.status = COMPLETE
        self.hire_service_2.save()

        client = APIClient()
        response = client.delete("/1.0/hire-services/{0}/".format(self.hire_service_2.pk), data={}, format='json',
                                 HTTP_AUTHORIZATION='Token {}'.format(token_jwt_1))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_cancel_hire_service_professional_ko_status_reject(self):
        professional = self.professional
        token_jwt_1 = jwt_encode(professional)

        self.hire_service_2.status = REJECT
        self.hire_service_2.save()

        client = APIClient()
        response = client.delete("/1.0/hire-services/{0}/".format(self.hire_service_2.pk), data={}, format='json',
                                 HTTP_AUTHORIZATION='Token {}'.format(token_jwt_1))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_cancel_hire_service_professional_ko_status_cancel(self):
        professional = self.professional
        token_jwt_1 = jwt_encode(professional)

        self.hire_service_2.status = CANCEL
        self.hire_service_2.save()

        client = APIClient()
        response = client.delete("/1.0/hire-services/{0}/".format(self.hire_service_2.pk), data={}, format='json',
                                 HTTP_AUTHORIZATION='Token {}'.format(token_jwt_1))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_cancel_hire_service_professional_ko_status_accept_date_passed(self):
        professional = self.professional
        token_jwt_1 = jwt_encode(professional)

        client = APIClient()
        response = client.delete("/1.0/hire-services/{0}/".format(self.hire_service_2.pk), data={}, format='json',
                                 HTTP_AUTHORIZATION='Token {}'.format(token_jwt_1))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
