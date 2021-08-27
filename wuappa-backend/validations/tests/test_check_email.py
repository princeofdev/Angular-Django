from django.contrib.auth.models import User
from django.test import override_settings, TestCase
from rest_framework import status
from rest_framework.test import APIClient


@override_settings(ROOT_URLCONF='validations.urls')
class TestCheckEmailAPI(TestCase):

    def test_check_email_ok(self):
        data = {
            "email": "prueba@kasfactory.net"
        }

        client = APIClient()
        response = client.post("/1.0/check-email/", data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_check_email_ko_email_not_sent(self):
        data = {}

        client = APIClient()
        response = client.post("/1.0/check-email/", data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_check_email_ko_email_sent_null(self):
        data = {
            "email": ""
        }

        client = APIClient()
        response = client.post("/1.0/check-email/", data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_check_email_ko_email_invalid(self):
        data = {
            "email": "aurora"
        }

        client = APIClient()
        response = client.post("/1.0/check-email/", data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_check_email_ko_email_user_already_exist(self):
        User.objects.create_user('testuser', email='prueba@kasfactory.net', password='testuser')
        data = {
            "email": "prueba@kasfactory.net"
        }

        client = APIClient()
        response = client.post("/1.0/check-email/", data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
