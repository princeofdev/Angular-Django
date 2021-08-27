from django.test import override_settings, TestCase
from rest_framework import status
from rest_framework.test import APIClient


@override_settings(ROOT_URLCONF='validations.urls')
class TestCheckPhoneAPI(TestCase):

    def test_check_phone_ok(self):
        data = {
            "phone": "+34661661661"
        }

        client = APIClient()
        response = client.post("/1.0/check-phone/", data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_check_phone_ko_phone_not_sent(self):
        data = {}

        client = APIClient()
        response = client.post("/1.0/check-phone/", data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_check_phone_ko_phone_sent_null(self):
        data = {
            "phone": ""
        }

        client = APIClient()
        response = client.post("/1.0/check-phone/", data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_check_phone_ko_phone_invalid_number(self):
        data = {
            "phone": "+346616616612"
        }

        client = APIClient()
        response = client.post("/1.0/check-phone/", data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_check_phone_ko_phone_invalid_prefix_not_sent(self):
        data = {
            "phone": "661661661"
        }

        client = APIClient()
        response = client.post("/1.0/check-phone/", data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
