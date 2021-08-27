from django.contrib.auth.models import User
from django.test import TestCase, override_settings
from rest_auth.utils import jwt_encode
from rest_framework import status
from rest_framework.test import APIClient

from services.models import Service


@override_settings(ROOT_URLCONF='services.urls')
class TestProfessionalAvailabilityServiceAPI(TestCase):
    fixtures = ['professional_availability.json']

    def setUp(self):
        self.final = User.objects.get(pk=2)

        self.service_1 = Service.objects.get(pk=1)
        self.service_2 = Service.objects.get(pk=2)
        self.service_3 = Service.objects.get(pk=3)

    def test_user_is_not_authenticate(self):
        data = {
          "services": [self.service_1.pk],
          "zip": "28029",
          "date": "2017-12-07",
          "time": "18:09"
        }

        client = APIClient()
        response = client.post("/1.0/professionals-availability/", data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_superuser_is_login_all_professional_available(self):
        superuser = User.objects.get(username='aurora')
        token_jwt_1 = jwt_encode(superuser)

        data = {
            "services": [self.service_1.pk],
            "zip": "28029",
            "date": "2028-12-01",
            "time": "18:09"
        }

        client = APIClient()
        response = client.post("/1.0/professionals-availability/", data=data, format='json',
                               HTTP_AUTHORIZATION='Token {}'.format(token_jwt_1))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()
        self.assertEqual(len(data), 3)

    def test_superuser_is_login_one_professional_available(self):
        superuser = User.objects.get(username='aurora')
        token_jwt_1 = jwt_encode(superuser)

        data = {
            "services": [self.service_1.pk],
            "zip": "28029",
            "date": "2028-12-07",
            "time": "18:09"
        }

        client = APIClient()
        response = client.post("/1.0/professionals-availability/", data=data, format='json',
                               HTTP_AUTHORIZATION='Token {}'.format(token_jwt_1))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()
        self.assertEqual(len(data), 1)

    def test_superuser_is_login_one_professional_available_more_than_one(self):
        superuser = User.objects.get(username='aurora')
        token_jwt_1 = jwt_encode(superuser)

        data = {
            "services": [self.service_1.pk],
            "zip": "28029",
            "date": "2028-12-06",
            "time": "18:09"
        }

        client = APIClient()
        response = client.post("/1.0/professionals-availability/", data=data, format='json',
                               HTTP_AUTHORIZATION='Token {}'.format(token_jwt_1))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()
        self.assertEqual(len(data), 2)

    def test_superuser_is_login_not_professional_available_days_off(self):
        superuser = User.objects.get(username='aurora')
        token_jwt_1 = jwt_encode(superuser)

        data = {
            "services": [self.service_1.pk],
            "zip": "28029",
            "date": "2028-12-03",
            "time": "11:15"
        }

        client = APIClient()
        response = client.post("/1.0/professionals-availability/", data=data, format='json',
                               HTTP_AUTHORIZATION='Token {}'.format(token_jwt_1))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()
        self.assertEqual(len(data), 0)

    def test_superuser_is_login_error_services_not_sent(self):
        superuser = User.objects.get(username='aurora')
        token_jwt_1 = jwt_encode(superuser)

        data = {
            "zip": "28029",
            "date": "2017-12-06",
            "time": "18:09"
        }

        client = APIClient()
        response = client.post("/1.0/professionals-availability/", data=data, format='json',
                               HTTP_AUTHORIZATION='Token {}'.format(token_jwt_1))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_superuser_is_login_error_services_invalid(self):
        superuser = User.objects.get(username='aurora')
        token_jwt_1 = jwt_encode(superuser)

        data = {
            "services": [0],
            "zip": "28029",
            "date": "2017-12-06",
            "time": "18:09"
        }

        client = APIClient()
        response = client.post("/1.0/professionals-availability/", data=data, format='json',
                               HTTP_AUTHORIZATION='Token {}'.format(token_jwt_1))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_superuser_is_login_error_services_not_include_for_zip_workzone(self):
        superuser = User.objects.get(username='aurora')
        token_jwt_1 = jwt_encode(superuser)

        data = {
            "services": [self.service_2.pk],
            "zip": "28029",
            "date": "2017-12-01",
            "time": "11:40"
        }

        client = APIClient()
        response = client.post("/1.0/professionals-availability/", data=data, format='json',
                               HTTP_AUTHORIZATION='Token {}'.format(token_jwt_1))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_superuser_is_login_error_services_zip_sent(self):
        superuser = User.objects.get(username='aurora')
        token_jwt_1 = jwt_encode(superuser)

        data = {
            "services": [self.service_1.pk],
            "date": "2017-12-06",
            "time": "18:09"
        }

        client = APIClient()
        response = client.post("/1.0/professionals-availability/", data=data, format='json',
                               HTTP_AUTHORIZATION='Token {}'.format(token_jwt_1))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_superuser_is_login_error_zip_invalid(self):
        superuser = User.objects.get(username='aurora')
        token_jwt_1 = jwt_encode(superuser)

        data = {
            "services": [self.service_1.pk],
            "zip": "",
            "date": "2017-12-06",
            "time": "18:09"
        }

        client = APIClient()
        response = client.post("/1.0/professionals-availability/", data=data, format='json',
                               HTTP_AUTHORIZATION='Token {}'.format(token_jwt_1))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_superuser_is_login_error_date_not_sent(self):
        superuser = User.objects.get(username='aurora')
        token_jwt_1 = jwt_encode(superuser)

        data = {
            "services": [self.service_1.pk],
            "zip": "28029",
            "time": "18:09"
        }

        client = APIClient()
        response = client.post("/1.0/professionals-availability/", data=data, format='json',
                               HTTP_AUTHORIZATION='Token {}'.format(token_jwt_1))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_superuser_is_login_error_date_invalid(self):
        superuser = User.objects.get(username='aurora')
        token_jwt_1 = jwt_encode(superuser)

        data = {
            "services": [self.service_1.pk],
            "zip": "28029",
            "date": "06-12-2017",
            "time": "18:09"
        }

        client = APIClient()
        response = client.post("/1.0/professionals-availability/", data=data, format='json',
                               HTTP_AUTHORIZATION='Token {}'.format(token_jwt_1))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_superuser_is_login_error_time_not_sent(self):
        superuser = User.objects.get(username='aurora')
        token_jwt_1 = jwt_encode(superuser)

        data = {
            "services": [self.service_1.pk],
            "zip": "28029",
            "date": "2017-12-06"
        }

        client = APIClient()
        response = client.post("/1.0/professionals-availability/", data=data, format='json',
                               HTTP_AUTHORIZATION='Token {}'.format(token_jwt_1))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_superuser_is_login_error_time_invalid(self):
        superuser = User.objects.get(username='aurora')
        token_jwt_1 = jwt_encode(superuser)

        data = {
            "services": [self.service_1.pk],
            "zip": "28029",
            "date": "2017-12-06",
            "time": "34"
        }

        client = APIClient()
        response = client.post("/1.0/professionals-availability/", data=data, format='json',
                               HTTP_AUTHORIZATION='Token {}'.format(token_jwt_1))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
