import datetime
import json
from copy import deepcopy

from django.contrib.auth.models import User
from django.test import TestCase, override_settings
from django.utils.translation import ugettext_lazy as _
from djstripe.models import Card
from rest_auth.utils import jwt_encode
from rest_framework import status
from rest_framework.test import APIClient

from coupon.models import Coupon, UsedCoupon
from geo.models import WorkZone, City
from services.models import Service, CityServices
from . import FAKE_CUSTOMER, FAKE_CARD, FAKE_CARD_II, FAKE_CUSTOMER_II


@override_settings(ROOT_URLCONF='services.urls')
class TestCreateHireServiceAPI(TestCase):
    fixtures = ['registration_fixtures.json']

    def setUp(self):
        self.professional = User.objects.get(pk=1)
        self.final = User.objects.get(pk=2)

        self.service_1 = Service.objects.get(pk=1)
        self.service_2 = Service.objects.get(pk=2)
        self.service_3 = Service.objects.get(pk=3)

        self.coupon = Coupon.objects.create(code="BATMAN", amount_off=1, type="MON")

        city = City.objects.all()[0]
        WorkZone.objects.create(name="Test", zip_codes=[28039], city=city)
        CityServices.objects.create(city=city, service=self.service_1, price=3.0, price_currency='EUR')
        CityServices.objects.create(city=city, service=self.service_2, price=5.0, price_currency='EUR')
        CityServices.objects.create(city=city, service=self.service_3, price=7.0, price_currency='EUR')

    def test_user_is_not_authenticate(self):
        data = {
            "client": self.final.pk,
            "professional": self.professional.pk,
            "date": "2028-10-10",
            "time": "18:00:00",
            "address": "Aligustre 20",
            "city": "Madrid",
            "region": "Madrid",
            "country": "Spain",
            "zip_code": "28039",
            "services": [self.service_1.pk, self.service_3.pk],
            "comments": "Hola",
            "total": 10.00,
            "credit_card": FAKE_CARD["id"]
        }

        client = APIClient()
        response = client.post("/1.0/hire-services/", data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_hire_service_ok(self):
        superuser = User.objects.get(username='aurora')
        token_jwt_1 = jwt_encode(superuser)
        self.customer = FAKE_CUSTOMER.create_for_user(self.final)
        Card.sync_from_stripe_data(deepcopy(FAKE_CARD))

        data = {
            "client": self.final.pk,
            "professional": self.professional.pk,
            "date": "2028-10-10",
            "time": "18:00:00",
            "address": "Aligustre 20",
            "city": "Madrid",
            "region": "Madrid",
            "country": "Spain",
            "zip_code": "28039",
            "services": [self.service_1.pk, self.service_3.pk],
            "comments": "Hola",
            "total": 10.00,
            "credit_card": FAKE_CARD["id"]
        }

        client = APIClient()
        response = client.post("/1.0/hire-services/", data=data, format='json',
                               HTTP_AUTHORIZATION='Token {}'.format(token_jwt_1))
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_hire_service_ok_included_currency(self):
        superuser = User.objects.get(username='aurora')
        token_jwt_1 = jwt_encode(superuser)
        self.customer = FAKE_CUSTOMER.create_for_user(self.final)
        Card.sync_from_stripe_data(deepcopy(FAKE_CARD))

        data = {
            "client": self.final.pk,
            "professional": self.professional.pk,
            "date": "2028-10-10",
            "time": "18:00:00",
            "address": "Aligustre 20",
            "city": "Madrid",
            "region": "Madrid",
            "country": "Spain",
            "zip_code": "28039",
            "services": [self.service_1.pk, self.service_3.pk],
            "comments": "Hola",
            "total": 10.00,
            "total_currency": "EUR",
            "credit_card": FAKE_CARD["id"]
        }

        client = APIClient()
        response = client.post("/1.0/hire-services/", data=data, format='json',
                               HTTP_AUTHORIZATION='Token {}'.format(token_jwt_1))
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_hire_service_ok_professional_not_sent(self):
        superuser = User.objects.get(username='aurora')
        token_jwt_1 = jwt_encode(superuser)
        self.customer = FAKE_CUSTOMER.create_for_user(self.final)
        Card.sync_from_stripe_data(deepcopy(FAKE_CARD))

        data = {
            "client": self.final.pk,
            "date": "2028-10-10",
            "time": "18:00:00",
            "address": "Aligustre 20",
            "city": "Madrid",
            "region": "Madrid",
            "country": "Spain",
            "zip_code": "28039",
            "services": [self.service_1.pk, self.service_3.pk],
            "comments": "Hola",
            "total": 10.00,
            "credit_card": FAKE_CARD["id"]
        }

        client = APIClient()
        response = client.post("/1.0/hire-services/", data=data, format='json',
                               HTTP_AUTHORIZATION='Token {}'.format(token_jwt_1))
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_hire_service_ko_client_not_sent(self):
        superuser = User.objects.get(username='aurora')
        token_jwt_1 = jwt_encode(superuser)
        self.customer = FAKE_CUSTOMER.create_for_user(self.professional)
        Card.sync_from_stripe_data(deepcopy(FAKE_CARD))

        data = {
            "professional": self.professional.pk,
            "date": "2028-10-10",
            "time": "18:00:00",
            "address": "Aligustre 20",
            "city": "Madrid",
            "region": "Madrid",
            "country": "Spain",
            "zip_code": "28039",
            "services": [self.service_1.pk, self.service_3.pk],
            "comments": "Hola",
            "total": 10.00,
            "credit_card": FAKE_CARD["id"]
        }

        client = APIClient()
        response = client.post("/1.0/hire-services/", data=data, format='json',
                               HTTP_AUTHORIZATION='Token {}'.format(token_jwt_1))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data.get('client')[0], _("This field is required."))

    def test_create_hire_service_ko_client_not_exist(self):
        superuser = User.objects.get(username='aurora')
        token_jwt_1 = jwt_encode(superuser)
        self.customer = FAKE_CUSTOMER.create_for_user(self.professional)
        Card.sync_from_stripe_data(deepcopy(FAKE_CARD))

        data = {
            "client": 0,
            "professional": self.professional.pk,
            "date": "2028-10-10",
            "time": "18:00:00",
            "address": "Aligustre 20",
            "city": "Madrid",
            "region": "Madrid",
            "country": "Spain",
            "zip_code": "28039",
            "services": [self.service_1.pk, self.service_3.pk],
            "comments": "Hola",
            "total": 10.00,
            "credit_card": FAKE_CARD["id"]
        }

        client = APIClient()
        response = client.post("/1.0/hire-services/", data=data, format='json',
                               HTTP_AUTHORIZATION='Token {}'.format(token_jwt_1))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data.get('client')[0], _("Invalid pk \"0\" - object does not exist."))

    def test_create_hire_service_ko_client_sent_a_professional(self):
        superuser = User.objects.get(username='aurora')
        token_jwt_1 = jwt_encode(superuser)
        self.customer = FAKE_CUSTOMER.create_for_user(self.professional)
        Card.sync_from_stripe_data(deepcopy(FAKE_CARD))

        data = {
            "client": self.professional.pk,
            "professional": self.professional.pk,
            "date": "2028-10-10",
            "time": "18:00:00",
            "address": "Aligustre 20",
            "city": "Madrid",
            "region": "Madrid",
            "country": "Spain",
            "zip_code": "28039",
            "services": [self.service_1.pk, self.service_3.pk],
            "comments": "Hola",
            "total": 10.00,
            "credit_card": FAKE_CARD["id"]
        }

        client = APIClient()
        response = client.post("/1.0/hire-services/", data=data, format='json',
                               HTTP_AUTHORIZATION='Token {}'.format(token_jwt_1))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data.get('non_field_errors')[0],
                         _("Client user must be a final client, not professional"))

    def test_create_hire_service_ko_professional_not_exist(self):
        superuser = User.objects.get(username='aurora')
        token_jwt_1 = jwt_encode(superuser)
        self.customer = FAKE_CUSTOMER.create_for_user(self.final)
        Card.sync_from_stripe_data(deepcopy(FAKE_CARD))

        data = {
            "client": self.final.pk,
            "professional": 0,
            "date": "2028-10-10",
            "time": "18:00:00",
            "address": "Aligustre 20",
            "city": "Madrid",
            "region": "Madrid",
            "country": "Spain",
            "zip_code": "28039",
            "services": [self.service_1.pk, self.service_3.pk],
            "comments": "Hola",
            "total": 10.00,
            "credit_card": FAKE_CARD["id"]
        }

        client = APIClient()
        response = client.post("/1.0/hire-services/", data=data, format='json',
                               HTTP_AUTHORIZATION='Token {}'.format(token_jwt_1))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data.get('professional')[0], _("Invalid pk \"0\" - object does not exist."))

    def test_create_hire_service_ko_professional_sent_a_final(self):
        superuser = User.objects.get(username='aurora')
        token_jwt_1 = jwt_encode(superuser)
        self.customer = FAKE_CUSTOMER.create_for_user(self.final)
        Card.sync_from_stripe_data(deepcopy(FAKE_CARD))

        data = {
            "client": self.final.pk,
            "professional": self.final.pk,
            "date": "2028-10-10",
            "time": "18:00:00",
            "address": "Aligustre 20",
            "city": "Madrid",
            "region": "Madrid",
            "country": "Spain",
            "zip_code": "28039",
            "services": [self.service_1.pk, self.service_3.pk],
            "comments": "Hola",
            "total": 10.00,
            "credit_card": FAKE_CARD["id"]
        }

        client = APIClient()
        response = client.post("/1.0/hire-services/", data=data, format='json',
                               HTTP_AUTHORIZATION='Token {}'.format(token_jwt_1))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data.get('non_field_errors')[0], _("Professional user must be a professional"))

    def test_create_hire_service_ko_date_not_sent(self):
        superuser = User.objects.get(username='aurora')
        token_jwt_1 = jwt_encode(superuser)
        self.customer = FAKE_CUSTOMER.create_for_user(self.final)
        Card.sync_from_stripe_data(deepcopy(FAKE_CARD))

        data = {
            "client": self.final.pk,
            "professional": self.professional.pk,
            "time": "18:00:00",
            "address": "Aligustre 20",
            "city": "Madrid",
            "region": "Madrid",
            "country": "Spain",
            "zip_code": "28039",
            "services": [self.service_1.pk, self.service_3.pk],
            "comments": "Hola",
            "total": 10.00,
            "credit_card": FAKE_CARD["id"]
        }

        client = APIClient()
        response = client.post("/1.0/hire-services/", data=data, format='json',
                               HTTP_AUTHORIZATION='Token {}'.format(token_jwt_1))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data.get('date')[0], _("This field is required."))

    def test_create_hire_service_ko_date_invalid_format(self):
        superuser = User.objects.get(username='aurora')
        token_jwt_1 = jwt_encode(superuser)
        self.customer = FAKE_CUSTOMER.create_for_user(self.final)
        Card.sync_from_stripe_data(deepcopy(FAKE_CARD))

        data = {
            "client": self.final.pk,
            "professional": self.professional.pk,
            "date": "10-10-2017",
            "time": "18:00:00",
            "address": "Aligustre 20",
            "city": "Madrid",
            "region": "Madrid",
            "country": "Spain",
            "zip_code": "28039",
            "services": [self.service_1.pk, self.service_3.pk],
            "comments": "Hola",
            "total": 10.00,
            "credit_card": FAKE_CARD["id"]
        }

        client = APIClient()
        response = client.post("/1.0/hire-services/", data=data, format='json',
                               HTTP_AUTHORIZATION='Token {}'.format(token_jwt_1))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data.get('date')[0],
                         _("Date has wrong format. Use one of these formats instead: YYYY[-MM[-DD]]."))

    def test_create_hire_service_ko_time_not_sent(self):
        superuser = User.objects.get(username='aurora')
        token_jwt_1 = jwt_encode(superuser)
        self.customer = FAKE_CUSTOMER.create_for_user(self.final)
        Card.sync_from_stripe_data(deepcopy(FAKE_CARD))

        data = {
            "client": self.final.pk,
            "professional": self.professional.pk,
            "date": "2028-10-10",
            "address": "Aligustre 20",
            "city": "Madrid",
            "region": "Madrid",
            "country": "Spain",
            "zip_code": "28039",
            "services": [self.service_1.pk, self.service_3.pk],
            "comments": "Hola",
            "total": 10.00,
            "credit_card": FAKE_CARD["id"]
        }

        client = APIClient()
        response = client.post("/1.0/hire-services/", data=data, format='json',
                               HTTP_AUTHORIZATION='Token {}'.format(token_jwt_1))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data.get('time')[0], _("This field is required."))

    def test_create_hire_service_ko_time_invalid_format(self):
        superuser = User.objects.get(username='aurora')
        token_jwt_1 = jwt_encode(superuser)
        self.customer = FAKE_CUSTOMER.create_for_user(self.final)
        Card.sync_from_stripe_data(deepcopy(FAKE_CARD))

        data = {
            "client": self.final.pk,
            "professional": self.professional.pk,
            "date": "2028-10-10",
            "time": "18",
            "address": "Aligustre 20",
            "city": "Madrid",
            "region": "Madrid",
            "country": "Spain",
            "zip_code": "28039",
            "services": [self.service_1.pk, self.service_3.pk],
            "comments": "Hola",
            "total": 10.00,
            "credit_card": FAKE_CARD["id"]
        }

        client = APIClient()
        response = client.post("/1.0/hire-services/", data=data, format='json',
                               HTTP_AUTHORIZATION='Token {}'.format(token_jwt_1))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data.get('time')[0],
                         _("Time has wrong format. Use one of these formats instead: hh:mm[:ss[.uuuuuu]]."))

    def test_create_hire_service_ko_address_not_sent(self):
        superuser = User.objects.get(username='aurora')
        token_jwt_1 = jwt_encode(superuser)
        self.customer = FAKE_CUSTOMER.create_for_user(self.final)
        Card.sync_from_stripe_data(deepcopy(FAKE_CARD))

        data = {
            "client": self.final.pk,
            "professional": self.professional.pk,
            "date": "2028-10-10",
            "time": "18:00:00",
            "city": "Madrid",
            "region": "Madrid",
            "country": "Spain",
            "zip_code": "28039",
            "services": [self.service_1.pk, self.service_3.pk],
            "comments": "Hola",
            "total": 10.00,
            "credit_card": FAKE_CARD["id"]
        }

        client = APIClient()
        response = client.post("/1.0/hire-services/", data=data, format='json',
                               HTTP_AUTHORIZATION='Token {}'.format(token_jwt_1))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data.get('address')[0], _("This field is required."))

    def test_create_hire_service_ko_address_sent_null(self):
        superuser = User.objects.get(username='aurora')
        token_jwt_1 = jwt_encode(superuser)
        self.customer = FAKE_CUSTOMER.create_for_user(self.final)
        Card.sync_from_stripe_data(deepcopy(FAKE_CARD))

        data = {
            "client": self.final.pk,
            "professional": self.professional.pk,
            "date": "2028-10-10",
            "time": "18:00:00",
            "address": "",
            "city": "Madrid",
            "region": "Madrid",
            "country": "Spain",
            "zip_code": "28039",
            "services": [self.service_1.pk, self.service_3.pk],
            "comments": "Hola",
            "total": 10.00,
            "credit_card": FAKE_CARD["id"]
        }

        client = APIClient()
        response = client.post("/1.0/hire-services/", data=data, format='json',
                               HTTP_AUTHORIZATION='Token {}'.format(token_jwt_1))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data.get('address')[0], _("This field may not be blank."))

    def test_create_hire_service_ko_city_not_sent(self):
        superuser = User.objects.get(username='aurora')
        token_jwt_1 = jwt_encode(superuser)
        self.customer = FAKE_CUSTOMER.create_for_user(self.final)
        Card.sync_from_stripe_data(deepcopy(FAKE_CARD))

        data = {
            "client": self.final.pk,
            "professional": self.professional.pk,
            "date": "2028-10-10",
            "time": "18:00:00",
            "address": "Aligustre 20",
            "region": "Madrid",
            "country": "Spain",
            "zip_code": "28039",
            "services": [self.service_1.pk, self.service_3.pk],
            "comments": "Hola",
            "total": 10.00,
            "credit_card": FAKE_CARD["id"]
        }

        client = APIClient()
        response = client.post("/1.0/hire-services/", data=data, format='json',
                               HTTP_AUTHORIZATION='Token {}'.format(token_jwt_1))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data.get('city')[0], _("This field is required."))

    def test_create_hire_service_ko_city_sent_null(self):
        superuser = User.objects.get(username='aurora')
        token_jwt_1 = jwt_encode(superuser)
        self.customer = FAKE_CUSTOMER.create_for_user(self.final)
        Card.sync_from_stripe_data(deepcopy(FAKE_CARD))

        data = {
            "client": self.final.pk,
            "professional": self.professional.pk,
            "date": "2028-10-10",
            "time": "18:00:00",
            "address": "Aligustre 20",
            "city": "",
            "region": "Madrid",
            "country": "Spain",
            "zip_code": "28039",
            "services": [self.service_1.pk, self.service_3.pk],
            "comments": "Hola",
            "total": 10.00,
            "credit_card": FAKE_CARD["id"]
        }

        client = APIClient()
        response = client.post("/1.0/hire-services/", data=data, format='json',
                               HTTP_AUTHORIZATION='Token {}'.format(token_jwt_1))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data.get('city')[0], _("This field may not be blank."))

    def test_create_hire_service_ko_region_not_sent(self):
        superuser = User.objects.get(username='aurora')
        token_jwt_1 = jwt_encode(superuser)
        self.customer = FAKE_CUSTOMER.create_for_user(self.final)
        Card.sync_from_stripe_data(deepcopy(FAKE_CARD))

        data = {
            "client": self.final.pk,
            "professional": self.professional.pk,
            "date": "2028-10-10",
            "time": "18:00:00",
            "address": "Aligustre 20",
            "city": "Madrid",
            "country": "Spain",
            "zip_code": "28039",
            "services": [self.service_1.pk, self.service_3.pk],
            "comments": "Hola",
            "total": 10.00,
            "credit_card": FAKE_CARD["id"]
        }

        client = APIClient()
        response = client.post("/1.0/hire-services/", data=data, format='json',
                               HTTP_AUTHORIZATION='Token {}'.format(token_jwt_1))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data.get('region')[0], _("This field is required."))

    def test_create_hire_service_ko_region_sent_null(self):
        superuser = User.objects.get(username='aurora')
        token_jwt_1 = jwt_encode(superuser)
        self.customer = FAKE_CUSTOMER.create_for_user(self.final)
        Card.sync_from_stripe_data(deepcopy(FAKE_CARD))

        data = {
            "client": self.final.pk,
            "professional": self.professional.pk,
            "date": "2028-10-10",
            "time": "18:00:00",
            "address": "Aligustre 20",
            "city": "Madrid",
            "region": "",
            "country": "Spain",
            "zip_code": "28039",
            "services": [self.service_1.pk, self.service_3.pk],
            "comments": "Hola",
            "total": 10.00,
            "credit_card": FAKE_CARD["id"]
        }

        client = APIClient()
        response = client.post("/1.0/hire-services/", data=data, format='json',
                               HTTP_AUTHORIZATION='Token {}'.format(token_jwt_1))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data.get('region')[0], _("This field may not be blank."))

    def test_create_hire_service_ko_country_not_sent(self):
        superuser = User.objects.get(username='aurora')
        token_jwt_1 = jwt_encode(superuser)
        self.customer = FAKE_CUSTOMER.create_for_user(self.final)
        Card.sync_from_stripe_data(deepcopy(FAKE_CARD))

        data = {
            "client": self.final.pk,
            "professional": self.professional.pk,
            "date": "2028-10-10",
            "time": "18:00:00",
            "address": "Aligustre 20",
            "city": "Madrid",
            "region": "Madrid",
            "zip_code": "28039",
            "services": [self.service_1.pk, self.service_3.pk],
            "comments": "Hola",
            "total": 10.00,
            "credit_card": FAKE_CARD["id"]
        }

        client = APIClient()
        response = client.post("/1.0/hire-services/", data=data, format='json',
                               HTTP_AUTHORIZATION='Token {}'.format(token_jwt_1))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data.get('country')[0], _("This field is required."))

    def test_create_hire_service_ko_country_sent_null(self):
        superuser = User.objects.get(username='aurora')
        token_jwt_1 = jwt_encode(superuser)
        self.customer = FAKE_CUSTOMER.create_for_user(self.final)
        Card.sync_from_stripe_data(deepcopy(FAKE_CARD))

        data = {
            "client": self.final.pk,
            "professional": self.professional.pk,
            "date": "2028-10-10",
            "time": "18:00:00",
            "address": "Aligustre 20",
            "city": "Madrid",
            "region": "Madrid",
            "country": "",
            "zip_code": "28039",
            "services": [self.service_1.pk, self.service_3.pk],
            "comments": "Hola",
            "total": 10.00,
            "credit_card": FAKE_CARD["id"]
        }

        client = APIClient()
        response = client.post("/1.0/hire-services/", data=data, format='json',
                               HTTP_AUTHORIZATION='Token {}'.format(token_jwt_1))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data.get('country')[0], _("This field may not be blank."))

    def test_create_hire_service_ko_zip_not_sent(self):
        superuser = User.objects.get(username='aurora')
        token_jwt_1 = jwt_encode(superuser)
        self.customer = FAKE_CUSTOMER.create_for_user(self.final)
        Card.sync_from_stripe_data(deepcopy(FAKE_CARD))

        data = {
            "client": self.final.pk,
            "professional": self.professional.pk,
            "date": "2028-10-10",
            "time": "18:00:00",
            "address": "Aligustre 20",
            "city": "Madrid",
            "region": "Madrid",
            "country": "Spain",
            "services": [self.service_1.pk, self.service_3.pk],
            "comments": "Hola",
            "total": 10.00,
            "credit_card": FAKE_CARD["id"]
        }

        client = APIClient()
        response = client.post("/1.0/hire-services/", data=data, format='json',
                               HTTP_AUTHORIZATION='Token {}'.format(token_jwt_1))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data.get('zip_code')[0], _("This field is required."))

    def test_create_hire_service_ko_zip_sent_null(self):
        superuser = User.objects.get(username='aurora')
        token_jwt_1 = jwt_encode(superuser)
        self.customer = FAKE_CUSTOMER.create_for_user(self.final)
        Card.sync_from_stripe_data(deepcopy(FAKE_CARD))

        data = {
            "client": self.final.pk,
            "professional": self.professional.pk,
            "date": "2028-10-10",
            "time": "18:00:00",
            "address": "Aligustre 20",
            "city": "Madrid",
            "region": "Madrid",
            "country": "Spain",
            "zip_code": "",
            "services": [self.service_1.pk, self.service_3.pk],
            "comments": "Hola",
            "total": 10.00,
            "credit_card": FAKE_CARD["id"]
        }

        client = APIClient()
        response = client.post("/1.0/hire-services/", data=data, format='json',
                               HTTP_AUTHORIZATION='Token {}'.format(token_jwt_1))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data.get('zip_code')[0], _("This field may not be blank."))

    def test_create_hire_service_ko_services_not_sent(self):
        superuser = User.objects.get(username='aurora')
        token_jwt_1 = jwt_encode(superuser)
        self.customer = FAKE_CUSTOMER.create_for_user(self.final)
        Card.sync_from_stripe_data(deepcopy(FAKE_CARD))

        data = {
            "client": self.final.pk,
            "professional": self.professional.pk,
            "date": "2028-10-10",
            "time": "18:00:00",
            "address": "Aligustre 20",
            "city": "Madrid",
            "region": "Madrid",
            "country": "Spain",
            "zip_code": "28039",
            "comments": "Hola",
            "total": 10.00,
            "credit_card": FAKE_CARD["id"]
        }

        client = APIClient()
        response = client.post("/1.0/hire-services/", data=data, format='json',
                               HTTP_AUTHORIZATION='Token {}'.format(token_jwt_1))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data.get('services')[0], _("This field is required."))

    def test_create_hire_service_ko_services_sent_null(self):
        superuser = User.objects.get(username='aurora')
        token_jwt_1 = jwt_encode(superuser)
        self.customer = FAKE_CUSTOMER.create_for_user(self.final)
        Card.sync_from_stripe_data(deepcopy(FAKE_CARD))

        data = {
            "client": self.final.pk,
            "professional": self.professional.pk,
            "date": "2028-10-10",
            "time": "18:00:00",
            "address": "Aligustre 20",
            "city": "Madrid",
            "region": "Madrid",
            "country": "Spain",
            "zip_code": "28039",
            "services": [],
            "comments": "Hola",
            "total": 10.00,
            "credit_card": FAKE_CARD["id"]
        }

        client = APIClient()
        response = client.post("/1.0/hire-services/", data=data, format='json',
                               HTTP_AUTHORIZATION='Token {}'.format(token_jwt_1))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data.get('services')[0], _("This list may not be empty."))

    def test_create_hire_service_ko_services_not_exist(self):
        superuser = User.objects.get(username='aurora')
        token_jwt_1 = jwt_encode(superuser)
        self.customer = FAKE_CUSTOMER.create_for_user(self.final)
        Card.sync_from_stripe_data(deepcopy(FAKE_CARD))

        data = {
            "client": self.final.pk,
            "professional": self.professional.pk,
            "date": "2028-10-10",
            "time": "18:00:00",
            "address": "Aligustre 20",
            "city": "Madrid",
            "region": "Madrid",
            "country": "Spain",
            "zip_code": "28039",
            "services": [self.service_1.pk, self.service_3.pk, 0],
            "comments": "Hola",
            "total": 10.00,
            "credit_card": FAKE_CARD["id"]
        }

        client = APIClient()
        response = client.post("/1.0/hire-services/", data=data, format='json',
                               HTTP_AUTHORIZATION='Token {}'.format(token_jwt_1))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data.get('services')[0], _("Invalid pk \"0\" - object does not exist."))

    def test_create_hire_service_ko_total_not_sent(self):
        superuser = User.objects.get(username='aurora')
        token_jwt_1 = jwt_encode(superuser)
        self.customer = FAKE_CUSTOMER.create_for_user(self.final)
        Card.sync_from_stripe_data(deepcopy(FAKE_CARD))

        data = {
            "client": self.final.pk,
            "professional": self.professional.pk,
            "date": "2028-10-10",
            "time": "18:00:00",
            "address": "Aligustre 20",
            "city": "Madrid",
            "region": "Madrid",
            "country": "Spain",
            "zip_code": "28039",
            "services": [self.service_1.pk, self.service_3.pk],
            "comments": "Hola",
            "credit_card": FAKE_CARD["id"]
        }

        client = APIClient()
        response = client.post("/1.0/hire-services/", data=data, format='json',
                               HTTP_AUTHORIZATION='Token {}'.format(token_jwt_1))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data.get('non_field_errors')[0], _("Total amount_must_be_included"))

    def test_create_hire_service_ko_total_sent_null(self):
        superuser = User.objects.get(username='aurora')
        token_jwt_1 = jwt_encode(superuser)
        self.customer = FAKE_CUSTOMER.create_for_user(self.final)
        Card.sync_from_stripe_data(deepcopy(FAKE_CARD))

        data = {
            "client": self.final.pk,
            "professional": self.professional.pk,
            "date": "2028-10-10",
            "time": "18:00:00",
            "address": "Aligustre 20",
            "city": "Madrid",
            "region": "Madrid",
            "country": "Spain",
            "zip_code": "28039",
            "services": [self.service_1.pk, self.service_3.pk],
            "comments": "Hola",
            "total": "",
            "credit_card": FAKE_CARD["id"]
        }

        client = APIClient()
        response = client.post("/1.0/hire-services/", data=data, format='json',
                               HTTP_AUTHORIZATION='Token {}'.format(token_jwt_1))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data.get('total')[0], _("A valid number is required."))

    def test_create_hire_service_ko_credit_card_not_sent(self):
        superuser = User.objects.get(username='aurora')
        token_jwt_1 = jwt_encode(superuser)
        self.customer = FAKE_CUSTOMER.create_for_user(self.final)
        Card.sync_from_stripe_data(deepcopy(FAKE_CARD))

        data = {
            "client": self.final.pk,
            "professional": self.professional.pk,
            "date": "2028-10-10",
            "time": "18:00:00",
            "address": "Aligustre 20",
            "city": "Madrid",
            "region": "Madrid",
            "country": "Spain",
            "zip_code": "28039",
            "services": [self.service_1.pk, self.service_3.pk],
            "comments": "Hola",
            "total": 10.00
        }

        client = APIClient()
        response = client.post("/1.0/hire-services/", data=data, format='json',
                               HTTP_AUTHORIZATION='Token {}'.format(token_jwt_1))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data.get('credit_card')[0], _("This field is required."))

    def test_create_hire_service_ko_credit_card_sent_null(self):
        superuser = User.objects.get(username='aurora')
        token_jwt_1 = jwt_encode(superuser)
        self.customer = FAKE_CUSTOMER.create_for_user(self.final)
        Card.sync_from_stripe_data(deepcopy(FAKE_CARD))

        data = {
            "client": self.final.pk,
            "professional": self.professional.pk,
            "date": "2028-10-10",
            "time": "18:00:00",
            "address": "Aligustre 20",
            "city": "Madrid",
            "region": "Madrid",
            "country": "Spain",
            "zip_code": "28039",
            "services": [self.service_1.pk, self.service_3.pk],
            "comments": "Hola",
            "total": 10.00,
            "credit_card": ""
        }

        client = APIClient()
        response = client.post("/1.0/hire-services/", data=data, format='json',
                               HTTP_AUTHORIZATION='Token {}'.format(token_jwt_1))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data.get('credit_card')[0], _("This field may not be blank."))

    def test_create_hire_service_ko_credit_card_card_not_exist(self):
        superuser = User.objects.get(username='aurora')
        token_jwt_1 = jwt_encode(superuser)
        self.customer = FAKE_CUSTOMER.create_for_user(self.final)
        Card.sync_from_stripe_data(deepcopy(FAKE_CARD))

        data = {
            "client": self.final.pk,
            "professional": self.professional.pk,
            "date": "2028-10-10",
            "time": "18:00:00",
            "address": "Aligustre 20",
            "city": "Madrid",
            "region": "Madrid",
            "country": "Spain",
            "zip_code": "28039",
            "services": [self.service_1.pk, self.service_3.pk],
            "comments": "Hola",
            "total": 10.00,
            "credit_card": FAKE_CARD_II["id"]
        }

        client = APIClient()
        response = client.post("/1.0/hire-services/", data=data, format='json',
                               HTTP_AUTHORIZATION='Token {}'.format(token_jwt_1))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data.get('credit_card')[0], _("Credit card id is not included in app."))

    def test_create_hire_service_ko_credit_card_card_not_belongs_to_client(self):
        superuser = User.objects.get(username='aurora')
        token_jwt_1 = jwt_encode(superuser)
        self.customer = FAKE_CUSTOMER.create_for_user(self.final)
        Card.sync_from_stripe_data(deepcopy(FAKE_CARD))

        self.customer_2 = FAKE_CUSTOMER_II.create_for_user(self.professional)
        Card.sync_from_stripe_data(deepcopy(FAKE_CARD_II))

        data = {
            "client": self.final.pk,
            "professional": self.professional.pk,
            "date": "2028-10-10",
            "time": "18:00:00",
            "address": "Aligustre 20",
            "city": "Madrid",
            "region": "Madrid",
            "country": "Spain",
            "zip_code": "28039",
            "services": [self.service_1.pk, self.service_3.pk],
            "comments": "Hola",
            "total": 10.00,
            "credit_card": FAKE_CARD_II["id"]
        }

        client = APIClient()
        response = client.post("/1.0/hire-services/", data=data, format='json',
                               HTTP_AUTHORIZATION='Token {}'.format(token_jwt_1))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data.get('non_field_errors')[0], _("Credit card number not belongs to the client"))

    def test_create_hire_service_ko_datetime_less_than_two_hours(self):
        superuser = User.objects.get(username='aurora')
        token_jwt_1 = jwt_encode(superuser)
        self.customer = FAKE_CUSTOMER.create_for_user(self.final)
        Card.sync_from_stripe_data(deepcopy(FAKE_CARD))

        self.customer_2 = FAKE_CUSTOMER_II.create_for_user(self.professional)
        Card.sync_from_stripe_data(deepcopy(FAKE_CARD_II))

        service_datetime = datetime.datetime.now()
        time = datetime.datetime.now() + datetime.timedelta(hours=1)

        data = {
            "client": self.final.pk,
            "professional": self.professional.pk,
            "date": service_datetime.strftime('%Y-%m-%d'),
            "time": time.strftime('%H:%M:%S'),
            "address": "Aligustre 20",
            "city": "Madrid",
            "region": "Madrid",
            "country": "Spain",
            "zip_code": "28039",
            "services": [self.service_1.pk, self.service_3.pk],
            "comments": "Hola",
            "total": 10.00,
            "credit_card": FAKE_CARD["id"]
        }

        client = APIClient()
        response = client.post("/1.0/hire-services/", data=data, format='json',
                               HTTP_AUTHORIZATION='Token {}'.format(token_jwt_1))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data.get('non_field_errors')[0], _("The selected date is not enough to hire services."))

    def test_create_hire_service_with_valid_coupon_and_coupon_is_invalidated(self):
        self.customer = FAKE_CUSTOMER.create_for_user(self.final)
        Card.sync_from_stripe_data(deepcopy(FAKE_CARD))

        data = {
            "client": self.final.pk,
            "professional": self.professional.pk,
            "date": "2028-10-10",
            "time": "18:00:00",
            "address": "Aligustre 20",
            "city": "Madrid",
            "region": "Madrid",
            "country": "Spain",
            "zip_code": "28039",
            "services": [self.service_1.pk, self.service_3.pk],
            "comments": "Hola",
            "total": 9.00,
            "credit_card": FAKE_CARD["id"],
            "coupon": self.coupon.code
        }

        client = APIClient()
        client.force_authenticate(user=self.final)
        response = client.post("/1.0/hire-services/", json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Coupon.objects.get(code=self.coupon.code).valid)

        response = self.client.get("/api/1.0/coupon/{0}".format(self.coupon.code))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_hire_service_with_invalid_coupon(self):
        self.customer = FAKE_CUSTOMER.create_for_user(self.final)
        Card.sync_from_stripe_data(deepcopy(FAKE_CARD))

        data = {
            "client": self.final.pk,
            "professional": self.professional.pk,
            "date": "2028-10-10",
            "time": "18:00:00",
            "address": "Aligustre 20",
            "city": "Madrid",
            "region": "Madrid",
            "country": "Spain",
            "zip_code": "28039",
            "services": [self.service_1.pk, self.service_3.pk],
            "comments": "Hola",
            "total": 9.00,
            "credit_card": FAKE_CARD["id"],
            "coupon": self.coupon.code
        }
        UsedCoupon.objects.create(coupon=self.coupon, user=self.final)
        client = APIClient()
        client.force_authenticate(user=self.final)
        client.post("/1.0/hire-services/", data)
        # Tries to use the coupon again
        response = client.post("/1.0/hire-services/", json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data.get("coupon", [''])[0], "Coupon does not exist or is already used")

    def test_create_hire_service_with_invalid_price(self):
        self.customer = FAKE_CUSTOMER.create_for_user(self.final)
        Card.sync_from_stripe_data(deepcopy(FAKE_CARD))

        data = {
            "client": self.final.pk,
            "professional": self.professional.pk,
            "date": "2028-10-10",
            "time": "18:00:00",
            "address": "Aligustre 20",
            "city": "Madrid",
            "region": "Madrid",
            "country": "Spain",
            "zip_code": "28039",
            "services": [self.service_1.pk, self.service_3.pk],
            "comments": "Hola",
            "total": 9.00,
            "credit_card": FAKE_CARD["id"]
        }

        client = APIClient()
        client.force_authenticate(user=self.final)
        response = client.post("/1.0/hire-services/", json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data.get("non_field_errors", [''])[0], "Invalid price")

    def test_create_hire_service_with_invalid_price_and_coupon(self):
        self.customer = FAKE_CUSTOMER.create_for_user(self.final)
        Card.sync_from_stripe_data(deepcopy(FAKE_CARD))

        data = {
            "client": self.final.pk,
            "professional": self.professional.pk,
            "date": "2028-10-10",
            "time": "18:00:00",
            "address": "Aligustre 20",
            "city": "Madrid",
            "region": "Madrid",
            "country": "Spain",
            "zip_code": "28039",
            "services": [self.service_1.pk, self.service_3.pk],
            "comments": "Hola",
            "total": 10.00,
            "credit_card": FAKE_CARD["id"],
            "coupon": self.coupon.code
        }

        client = APIClient()
        client.force_authenticate(user=self.final)
        response = client.post("/1.0/hire-services/", json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data.get("non_field_errors", [''])[0], "Invalid price")

    def test_create_hire_service_several_same_services(self):
        self.customer = FAKE_CUSTOMER.create_for_user(self.final)
        Card.sync_from_stripe_data(deepcopy(FAKE_CARD))

        data = {
            "client": self.final.pk,
            "professional": self.professional.pk,
            "date": "2028-10-10",
            "time": "18:00:00",
            "address": "Aligustre 20",
            "city": "Madrid",
            "region": "Madrid",
            "country": "Spain",
            "zip_code": "28039",
            "services": [self.service_1.pk, self.service_1.pk],
            "comments": "Hola",
            "total": 6.00,
            "credit_card": FAKE_CARD["id"]
        }

        client = APIClient()
        client.force_authenticate(user=self.final)
        response = client.post("/1.0/hire-services/", json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
