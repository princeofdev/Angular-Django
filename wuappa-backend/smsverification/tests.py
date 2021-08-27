from datetime import timedelta

import requests
import requests_mock

from django.test import TestCase, override_settings
from django.utils import timezone
from rest_framework.status import HTTP_502_BAD_GATEWAY, HTTP_400_BAD_REQUEST, HTTP_201_CREATED, HTTP_200_OK
from rest_framework.test import APIClient

from smsverification.exceptions import SMSSendException, InvalidCodeException
from smsverification.models import VerificationCode
from smsverification.settings import BROKER_ENDPOINT

session = requests.Session()
adapter = requests_mock.Adapter()
session.mount('mock', adapter)


@override_settings(ROOT_URLCONF='smsverification.urls')
class VerificationCodeRequestTestCase(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.phone = '+34678901234'

    def test_invalid_phone_number_returns_bad_request(self):
        error_message = '(1) The string supplied did not seem to be a phone number.'
        with requests_mock.mock() as m:
            m.post(BROKER_ENDPOINT, text='data')
            response = self.client.post("/1.0/sms-verification/request/", data={'phone': 'abzced'}, format='json')
            self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)
            self.assertEqual(response.data.get('phone'), [error_message])

    def test_valid_phone_number_creates_verification_code(self):
        with requests_mock.mock() as m:
            response_text = '{"message-count":1,"messages":[{"status":"OK","msgid":"1","dnr":"' + self.phone + '"}]}'
            m.post(BROKER_ENDPOINT, text=response_text)
            response = self.client.post("/1.0/sms-verification/request/", data={'phone': self.phone}, format='json')
            self.assertEqual(response.status_code, HTTP_201_CREATED)
            self.assertEqual(response.data.get('phone'), self.phone)
            self.assertEqual(1, VerificationCode.objects.filter(phone=self.phone, verification_date=None).count())

    def test_returns_bad_gateway_when_issues_with_sms_broker(self):
        with requests_mock.mock() as m:
            m.post(BROKER_ENDPOINT, exc=requests.exceptions.RequestException)
            response = self.client.post("/1.0/sms-verification/request/", data={'phone': self.phone}, format='json')
            self.assertEqual(response.status_code, HTTP_502_BAD_GATEWAY)
            self.assertEqual(response.data.get('detail'), SMSSendException.default_detail)

            m.post(BROKER_ENDPOINT, exc=requests.exceptions.ConnectionError)
            response = self.client.post("/1.0/sms-verification/request/", data={'phone': self.phone}, format='json')
            self.assertEqual(response.status_code, HTTP_502_BAD_GATEWAY)
            self.assertEqual(response.data.get('detail'), SMSSendException.default_detail)

            m.post(BROKER_ENDPOINT, exc=requests.exceptions.HTTPError)
            response = self.client.post("/1.0/sms-verification/request/", data={'phone': self.phone}, format='json')
            self.assertEqual(response.status_code, HTTP_502_BAD_GATEWAY)
            self.assertEqual(response.data.get('detail'), SMSSendException.default_detail)

    def test_returns_bad_gateway_when_broker_json_response_is_mal_formatted(self):
        with requests_mock.mock() as m:
            m.post(BROKER_ENDPOINT, text='{')  # bad json
            response = self.client.post("/1.0/sms-verification/request/", data={'phone': self.phone}, format='json')
            self.assertEqual(response.status_code, HTTP_502_BAD_GATEWAY)
            self.assertEqual(response.data.get('detail'), SMSSendException.default_detail)


@override_settings(ROOT_URLCONF='smsverification.urls')
class CodeVerificationTestCase(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.phone = '+34678901234'
        self.code = 'ABCDEF'

    def test_valid_code_is_set_as_verified(self):
        VerificationCode.objects.create(phone=self.phone, code=self.code)
        data = {'phone': self.phone, 'code': self.code}
        response = self.client.post("/1.0/sms-verification/verify/", data=data, format='json')
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertEqual(response.data.get('code'), "verified")
        number_of_unverified_codes = VerificationCode.objects.filter(
            phone=self.phone, code=self.code, verification_date__isnull=True
        ).count()
        self.assertEqual(0, number_of_unverified_codes)

    def test_expired_code_returns_bad_request(self):
        VerificationCode.objects.create(
            phone=self.phone, code=self.code, expiration_date=timezone.now() - timedelta(minutes=15)
        )
        data = {'phone': self.phone, 'code': self.code}
        response = self.client.post("/1.0/sms-verification/verify/", data=data, format='json')
        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data.get('detail'), InvalidCodeException.default_detail)

    def test_verified_code_returns_bad_request(self):
        VerificationCode.objects.create(phone=self.phone, code=self.code, verification_date=timezone.now())
        data = {'phone': self.phone, 'code': self.code}
        response = self.client.post("/1.0/sms-verification/verify/", data=data, format='json')
        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data.get('detail'), InvalidCodeException.default_detail)
