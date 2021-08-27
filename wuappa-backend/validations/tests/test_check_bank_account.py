from django.test import override_settings, TestCase
from rest_framework import status
from rest_framework.test import APIClient


@override_settings(ROOT_URLCONF='validations.urls')
class TestCheckBankAccountAPI(TestCase):

    def test_check_email_ok(self):
        data = {
            "iban_bank_account": "ES5221003179712200170953",
            "swift_bank_account": "CAGLESMMCOP"
        }

        client = APIClient()
        response = client.post("/1.0/check-bank-account/", data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_check_email_ko_iban_not_sent(self):
        data = {
            "swift_bank_account": "CAGLESMMCOP"
        }

        client = APIClient()
        response = client.post("/1.0/check-bank-account/", data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_check_email_ko_swift_not_sent(self):
        data = {
            "iban_bank_account": "ES5221003179712200170953"
        }

        client = APIClient()
        response = client.post("/1.0/check-bank-account/", data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_check_email_ko_iban_sent_null(self):
        data = {
            "iban_bank_account": "",
            "swift_bank_account": "CAGLESMMCOP"
        }

        client = APIClient()
        response = client.post("/1.0/check-bank-account/", data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_check_email_ko_swift_sent_null(self):
        data = {
            "iban_bank_account": "ES5221003179712200170953",
            "swift_bank_account": ""
        }

        client = APIClient()
        response = client.post("/1.0/check-bank-account/", data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_check_email_ko_iban_invalid(self):
        data = {
            "iban_bank_account": "ES52210031797122001709534",
            "swift_bank_account": "CAGLESMMCOP"
        }

        client = APIClient()
        response = client.post("/1.0/check-bank-account/", data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_check_email_ko_swift_invalid(self):
        data = {
            "iban_bank_account": "ES5221003179712200170953",
            "swift_bank_account": "CAGLESMMCO"
        }

        client = APIClient()
        response = client.post("/1.0/check-bank-account/", data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
