from django.contrib.auth.models import User
from django.test import override_settings, TestCase
from django.utils.translation import ugettext_lazy as _

from rest_auth.utils import jwt_encode
from rest_framework import status
from rest_framework.test import APIClient


@override_settings(ROOT_URLCONF='wuappa.urls')
class TestRetrieveUserDetailRegisterAPI(TestCase):
    fixtures = ['geo_production.json', 'registration_fixtures.json']

    def test_user_is_not_authenticate(self):
        client = APIClient()
        response = client.get("/api/1.0/user/", format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_user_ok(self):
        superuser = User.objects.get(username='aurora')
        token_jwt_1 = jwt_encode(superuser)

        client = APIClient()
        response = client.get('/api/1.0/user/', format='json', HTTP_AUTHORIZATION='Token {}'.format(token_jwt_1))
        self.assertEqual(response.status_code, status.HTTP_200_OK)


@override_settings(ROOT_URLCONF='wuappa.urls')
class TestPatchUserDetailRegisterAPI(TestCase):
    fixtures = ['geo_production.json', 'registration_fixtures.json']

    def test_user_is_not_authenticate(self):
        data = {
            "first_name": "Aurora",
            "last_name": "Barrios",
            "profile": {
                "phone": "+34661661662",
                "picture": "",
                "type": "FIN",
                "iban_bank_account": "ES5221003179712200170953",
                "swift_bank_account": "CAGLESMMCOP",
                "documents": ["http://www.facebook.com/", "http://www.google.es"],
                "work_days": [1, 2, 3, 4, 5],
                "work_hours": [11, 12, 13, 16, 17, 18, 19],
                "city": [598]
            },
            "new_zones": [1],
            "new_services": [1]
        }
        client = APIClient()
        response = client.patch("/api/1.0/user/", data=data,format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_user_final_ok(self):
        superuser = User.objects.get(username='prueba')
        token_jwt_1 = jwt_encode(superuser)

        data = {
            "first_name": "Aurora",
            "last_name": "Barrios",
            "profile": {
                "phone": "+34661661662",
                "picture": "",
                "type": "FIN",
                "iban_bank_account": "ES5221003179712200170953",
                "swift_bank_account": "CAGLESMMCOP",
                "documents": ["http://www.facebook.com/", "http://www.google.es"],
                "city": [598]
            }
        }

        client = APIClient()
        response = client.patch('/api/1.0/user/', data=data, format='json',
                                HTTP_AUTHORIZATION='Token {}'.format(token_jwt_1))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_professional_ok(self):
        superuser = User.objects.get(username='aurora')
        token_jwt_1 = jwt_encode(superuser)

        data = {
            "first_name": "Aurora",
            "last_name": "Barrios",
            "profile": {
                "phone": "+34661661662",
                "picture": "",
                "type": "PRO",
                "iban_bank_account": "ES5221003179712200170953",
                "swift_bank_account": "CAGLESMMCOP",
                "documents": ["http://www.facebook.com/", "http://www.google.es"],
                "work_days": [1, 2, 3, 4, 5],
                "work_hours": [11, 12, 13, 16, 17, 18, 19],
                "city": [598]
            },
            "new_zones": [1],
            "new_services": [1, 3]
        }

        client = APIClient()
        response = client.patch('/api/1.0/user/', data=data, format='json',
                                HTTP_AUTHORIZATION='Token {}'.format(token_jwt_1))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_professional_ok_add_city(self):
        superuser = User.objects.get(username='aurora')
        token_jwt_1 = jwt_encode(superuser)

        data = {
            "first_name": "Aurora",
            "last_name": "Barrios",
            "profile": {
                "phone": "+34661661662",
                "picture": "",
                "type": "PRO",
                "iban_bank_account": "ES5221003179712200170953",
                "swift_bank_account": "CAGLESMMCOP",
                "documents": ["http://www.facebook.com/", "http://www.google.es"],
                "work_days": [1, 2, 3, 4, 5],
                "work_hours": [11, 12, 13, 16, 17, 18, 19],
                "city": [598, 703]
            },
            "new_zones": [1],
            "new_services": [1, 3]
        }

        client = APIClient()
        response = client.patch('/api/1.0/user/', data=data, format='json',
                                HTTP_AUTHORIZATION='Token {}'.format(token_jwt_1))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_final_phone_not_sent_ok(self):
        superuser = User.objects.get(username='prueba')
        token_jwt_1 = jwt_encode(superuser)

        data = {
            "first_name": "Aurora",
            "last_name": "Barrios",
            "profile": {
                "picture": "",
                "type": "FIN",
                "iban_bank_account": "ES5221003179712200170953",
                "swift_bank_account": "CAGLESMMCOP",
                "documents": ["http://www.facebook.com/", "http://www.google.es"],
                "city": [598]
            }
        }

        client = APIClient()
        response = client.patch('/api/1.0/user/', data=data, format='json',
                                HTTP_AUTHORIZATION='Token {}'.format(token_jwt_1))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_final_ok_only_update_profile(self):
        superuser = User.objects.get(username='prueba')
        token_jwt_1 = jwt_encode(superuser)

        data = {
            "profile": {
                "phone": "+34661661662",
                "picture": "",
                "type": "FIN",
                "iban_bank_account": "ES5221003179712200170953",
                "swift_bank_account": "CAGLESMMCOP",
                "documents": ["http://www.facebook.com/", "http://www.google.es"],
                "city": [598]
            }
        }

        client = APIClient()
        response = client.patch('/api/1.0/user/', data=data, format='json',
                                HTTP_AUTHORIZATION='Token {}'.format(token_jwt_1))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_final_ko_sent_phone_null(self):
        superuser = User.objects.get(username='prueba')
        token_jwt_1 = jwt_encode(superuser)

        data = {
            "first_name": "Aurora",
            "last_name": "Barrios",
            "profile": {
                "phone": "",
                "picture": "",
                "type": "FIN",
                "iban_bank_account": "ES5221003179712200170953",
                "swift_bank_account": "CAGLESMMCOP",
                "documents": ["http://www.facebook.com/", "http://www.google.es"],
                "city": [598]
            }
        }

        client = APIClient()
        response = client.patch('/api/1.0/user/', data=data, format='json',
                                HTTP_AUTHORIZATION='Token {}'.format(token_jwt_1))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data.get('profile').get('phone')[0], _("This field may not be blank."))

    def test_user_final_ko_sent_phone_invalid(self):
        superuser = User.objects.get(username='prueba')
        token_jwt_1 = jwt_encode(superuser)

        data = {
            "first_name": "Aurora",
            "last_name": "Barrios",
            "profile": {
                "phone": "+346616616621",
                "picture": "",
                "type": "FIN",
                "iban_bank_account": "ES5221003179712200170953",
                "swift_bank_account": "CAGLESMMCOP",
                "documents": ["http://www.facebook.com/", "http://www.google.es"],
                "city": [598]
            }
        }

        client = APIClient()
        response = client.patch('/api/1.0/user/', data=data, format='json',
                                HTTP_AUTHORIZATION='Token {}'.format(token_jwt_1))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data.get('profile').get('phone')[0], _("This phone number is not valid."))

    def test_user_final_ko_sent_picture_invalid(self):
        superuser = User.objects.get(username='prueba')
        token_jwt_1 = jwt_encode(superuser)

        data = {
            "first_name": "Aurora",
            "last_name": "Barrios",
            "profile": {
                "phone": "+34661661662",
                "picture": "aaaa",
                "type": "FIN",
                "iban_bank_account": "ES5221003179712200170953",
                "swift_bank_account": "CAGLESMMCOP",
                "documents": ["http://www.facebook.com/", "http://www.google.es"],
                "city": [598]
            }
        }

        client = APIClient()
        response = client.patch('/api/1.0/user/', data=data, format='json',
                                HTTP_AUTHORIZATION='Token {}'.format(token_jwt_1))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data.get('profile').get('picture')[0], _("Enter a valid URL."))

    def test_user_final_ko_sent_document_url_invalid(self):
        superuser = User.objects.get(username='prueba')
        token_jwt_1 = jwt_encode(superuser)

        data = {
            "first_name": "Aurora",
            "last_name": "Barrios",
            "profile": {
                "phone": "+34661661662",
                "picture": "aaaa",
                "type": "FIN",
                "iban_bank_account": "ES5221003179712200170953",
                "swift_bank_account": "CAGLESMMCOP",
                "documents": ["aaa", "http://www.google.es"],
                "city": [598]
            }
        }

        client = APIClient()
        response = client.patch('/api/1.0/user/', data=data, format='json',
                                HTTP_AUTHORIZATION='Token {}'.format(token_jwt_1))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data.get('profile').get('documents')[0], _("Enter a valid URL."))

    def test_user_final_ko_sent_invalid_city(self):
        superuser = User.objects.get(username='prueba')
        token_jwt_1 = jwt_encode(superuser)

        data = {
            "first_name": "Aurora",
            "last_name": "Barrios",
            "profile": {
                "phone": "+34661661662",
                "picture": "",
                "type": "FIN",
                "iban_bank_account": "ES5221003179712200170953",
                "swift_bank_account": "CAGLESMMCOP",
                "documents": ["aaa", "http://www.google.es"],
                "city": [0]
            }
        }

        client = APIClient()
        response = client.patch('/api/1.0/user/', data=data, format='json',
                                HTTP_AUTHORIZATION='Token {}'.format(token_jwt_1))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data.get('profile').get('city')[0], _("This city is not valid."))

    def test_user_professional_ok_update_only_profile(self):
        superuser = User.objects.get(username='aurora')
        token_jwt_1 = jwt_encode(superuser)

        data = {
            "profile": {
                "phone": "+34661661662",
                "picture": "",
                "type": "PRO",
                "iban_bank_account": "ES5221003179712200170953",
                "swift_bank_account": "CAGLESMMCOP",
                "documents": ["http://www.facebook.com/", "http://www.google.es"],
                "city": [598]
            }
        }

        client = APIClient()
        response = client.patch('/api/1.0/user/', data=data, format='json',
                                HTTP_AUTHORIZATION='Token {}'.format(token_jwt_1))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_professional_ok_phone_not_sent(self):
        superuser = User.objects.get(username='aurora')
        token_jwt_1 = jwt_encode(superuser)

        data = {
            "first_name": "Aurora",
            "last_name": "Barrios",
            "profile": {
                "picture": "",
                "type": "PRO",
                "iban_bank_account": "ES5221003179712200170953",
                "swift_bank_account": "CAGLESMMCOP",
                "documents": ["http://www.facebook.com/", "http://www.google.es"],
                "city": [598]
            },
            "new_zones": [1],
            "new_services": [1, 3]
        }

        client = APIClient()
        response = client.patch('/api/1.0/user/', data=data, format='json',
                                HTTP_AUTHORIZATION='Token {}'.format(token_jwt_1))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_professional_phone_sent_null(self):
        superuser = User.objects.get(username='aurora')
        token_jwt_1 = jwt_encode(superuser)

        data = {
            "first_name": "Aurora",
            "last_name": "Barrios",
            "profile": {
                "picture": "",
                "phone": "",
                "type": "PRO",
                "iban_bank_account": "ES5221003179712200170953",
                "swift_bank_account": "CAGLESMMCOP",
                "documents": ["http://www.facebook.com/", "http://www.google.es"],
                "city": [598]
            },
            "new_zones": [1],
            "new_services": [1, 3]
        }

        client = APIClient()
        response = client.patch('/api/1.0/user/', data=data, format='json',
                                HTTP_AUTHORIZATION='Token {}'.format(token_jwt_1))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data.get('profile').get('phone')[0], _("This field may not be blank."))

    def test_user_professional_phone_invalid(self):
        superuser = User.objects.get(username='aurora')
        token_jwt_1 = jwt_encode(superuser)

        data = {
            "first_name": "Aurora",
            "last_name": "Barrios",
            "profile": {
                "phone": "+346616616621",
                "picture": "",
                "type": "PRO",
                "iban_bank_account": "ES5221003179712200170953",
                "swift_bank_account": "CAGLESMMCOP",
                "documents": ["http://www.facebook.com/", "http://www.google.es"],
                "city": [598]
            },
            "new_zones": [1],
            "new_services": [1, 3]
        }

        client = APIClient()
        response = client.patch('/api/1.0/user/', data=data, format='json',
                                HTTP_AUTHORIZATION='Token {}'.format(token_jwt_1))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data.get('profile').get('phone')[0], _("This phone number is not valid."))

    def test_user_professional_iban_invalid(self):
        superuser = User.objects.get(username='aurora')
        token_jwt_1 = jwt_encode(superuser)

        data = {
            "first_name": "Aurora",
            "last_name": "Barrios",
            "profile": {
                "phone": "+346616616621",
                "picture": "",
                "type": "PRO",
                "iban_bank_account": "ES52210031797122001709531",
                "swift_bank_account": "CAGLESMMCOP",
                "documents": ["http://www.facebook.com/", "http://www.google.es"],
                "city": [598]
            },
            "new_zones": [1],
            "new_services": [1, 3]
        }

        client = APIClient()
        response = client.patch('/api/1.0/user/', data=data, format='json',
                                HTTP_AUTHORIZATION='Token {}'.format(token_jwt_1))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data.get('profile').get('iban_bank_account')[0],
                         _("ES IBANs must contain 24 characters."))

    def test_user_professional_swift_invalid(self):
        superuser = User.objects.get(username='aurora')
        token_jwt_1 = jwt_encode(superuser)

        data = {
            "first_name": "Aurora",
            "last_name": "Barrios",
            "profile": {
                "phone": "+346616616621",
                "picture": "",
                "type": "PRO",
                "iban_bank_account": "ES5221003179712200170953",
                "swift_bank_account": "CAGLESMMCOPA",
                "documents": ["http://www.facebook.com/", "http://www.google.es"],
                "city": [598]
            },
            "new_zones": [1],
            "new_services": [1, 3]
        }

        client = APIClient()
        response = client.patch('/api/1.0/user/', data=data, format='json',
                                HTTP_AUTHORIZATION='Token {}'.format(token_jwt_1))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data.get('profile').get('swift_bank_account')[0],
                         _("A SWIFT-BIC is either 8 or 11 characters long."))

    def test_user_professional_iban_swift_to_null_invalid(self):
        superuser = User.objects.get(username='aurora')
        token_jwt_1 = jwt_encode(superuser)

        data = {
            "first_name": "Aurora",
            "last_name": "Barrios",
            "profile": {
                "phone": "+34661661662",
                "picture": "",
                "type": "PRO",
                "iban_bank_account": "",
                "swift_bank_account": "",
                "documents": ["http://www.facebook.com/", "http://www.google.es"],
                "city": [598]
            },
            "new_zones": [1],
            "new_services": [1, 3]
        }

        client = APIClient()
        response = client.patch('/api/1.0/user/', data=data, format='json',
                                HTTP_AUTHORIZATION='Token {}'.format(token_jwt_1))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data.get('profile').get('non_field_errors')[0],
                         _("Must include iban and swift account number."))

    def test_user_professional_sent_documents_to_null(self):
        superuser = User.objects.get(username='aurora')
        token_jwt_1 = jwt_encode(superuser)

        data = {
            "first_name": "Aurora",
            "last_name": "Barrios",
            "profile": {
                "phone": "+34661661662",
                "picture": "",
                "type": "PRO",
                "iban_bank_account": "ES5221003179712200170953",
                "swift_bank_account": "CAGLESMMCOP",
                "documents": [],
                "city": [598]
            },
            "new_zones": [1],
            "new_services": [1, 3]
        }

        client = APIClient()
        response = client.patch('/api/1.0/user/', data=data, format='json',
                                HTTP_AUTHORIZATION='Token {}'.format(token_jwt_1))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data.get('profile').get('non_field_errors')[0],
                         _("Must include one document at least"))

    def test_user_professional_sent_city_not_sent(self):
        superuser = User.objects.get(username='aurora')
        token_jwt_1 = jwt_encode(superuser)

        data = {
            "first_name": "Aurora",
            "last_name": "Barrios",
            "profile": {
                "phone": "+34661661662",
                "picture": "",
                "type": "PRO",
                "iban_bank_account": "ES5221003179712200170953",
                "swift_bank_account": "CAGLESMMCOP",
                "documents": ["http://www.facebook.com/", "http://www.google.es"]
            },
            "new_zones": [1],
            "new_services": [1, 3]
        }

        client = APIClient()
        response = client.patch('/api/1.0/user/', data=data, format='json',
                                HTTP_AUTHORIZATION='Token {}'.format(token_jwt_1))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data.get('profile').get('non_field_errors')[0],
                         _("Must include one city"))

    def test_user_professional_sent_city_to_null(self):
        superuser = User.objects.get(username='aurora')
        token_jwt_1 = jwt_encode(superuser)

        data = {
            "first_name": "Aurora",
            "last_name": "Barrios",
            "profile": {
                "phone": "+34661661662",
                "picture": "",
                "type": "PRO",
                "iban_bank_account": "ES5221003179712200170953",
                "swift_bank_account": "CAGLESMMCOP",
                "documents": ["http://www.facebook.com/", "http://www.google.es"],
                "city": ""
            },
            "new_zones": [1],
            "new_services": [1, 3]
        }

        client = APIClient()
        response = client.patch('/api/1.0/user/', data=data, format='json',
                                HTTP_AUTHORIZATION='Token {}'.format(token_jwt_1))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data.get('profile').get('city')[0],
                         _("Expected a list of items but got type \"str\"."))

    def test_user_professional_sent_invalid_city(self):
        superuser = User.objects.get(username='aurora')
        token_jwt_1 = jwt_encode(superuser)

        data = {
            "first_name": "Aurora",
            "last_name": "Barrios",
            "profile": {
                "phone": "+34661661662",
                "picture": "",
                "type": "PRO",
                "iban_bank_account": "ES5221003179712200170953",
                "swift_bank_account": "CAGLESMMCOP",
                "documents": ["http://www.facebook.com/", "http://www.google.es"],
                "city": [0]
            },
            "new_zones": [1],
            "new_services": [1, 3]
        }

        client = APIClient()
        response = client.patch('/api/1.0/user/', data=data, format='json',
                                HTTP_AUTHORIZATION='Token {}'.format(token_jwt_1))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data.get('profile').get('city')[0], _("This city is not valid."))

    def test_user_professional_sent_invalid_zone(self):
        superuser = User.objects.get(username='aurora')
        token_jwt_1 = jwt_encode(superuser)

        data = {
            "first_name": "Aurora",
            "last_name": "Barrios",
            "profile": {
                "phone": "+34661661662",
                "picture": "",
                "type": "PRO",
                "iban_bank_account": "ES5221003179712200170953",
                "swift_bank_account": "CAGLESMMCOP",
                "documents": ["http://www.facebook.com/", "http://www.google.es"],
                "city": [598]
            },
            "new_zones": [1, 0],
            "new_services": [1, 3]
        }

        client = APIClient()
        response = client.patch('/api/1.0/user/', data=data, format='json',
                                HTTP_AUTHORIZATION='Token {}'.format(token_jwt_1))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data.get('new_zones')[0], _("Invalid pk \"0\" - object does not exist."))

    def test_user_professional_sent_invalid_service(self):
        superuser = User.objects.get(username='aurora')
        token_jwt_1 = jwt_encode(superuser)

        data = {
            "first_name": "Aurora",
            "last_name": "Barrios",
            "profile": {
                "phone": "+34661661662",
                "picture": "",
                "type": "PRO",
                "iban_bank_account": "ES5221003179712200170953",
                "swift_bank_account": "CAGLESMMCOP",
                "documents": ["http://www.facebook.com/", "http://www.google.es"],
                "city": [598]
            },
            "new_zones": [1],
            "new_services": [1, 3, 0]
        }

        client = APIClient()
        response = client.patch('/api/1.0/user/', data=data, format='json',
                                HTTP_AUTHORIZATION='Token {}'.format(token_jwt_1))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data.get('new_services')[0], _("Invalid pk \"0\" - object does not exist."))

    def test_user_professional_sent_invalid_work_days(self):
        superuser = User.objects.get(username='aurora')
        token_jwt_1 = jwt_encode(superuser)

        data = {
            "first_name": "Aurora",
            "last_name": "Barrios",
            "profile": {
                "phone": "+34661661662",
                "picture": "",
                "type": "PRO",
                "iban_bank_account": "ES5221003179712200170953",
                "swift_bank_account": "CAGLESMMCOP",
                "documents": ["http://www.facebook.com/", "http://www.google.es"],
                "work_days": [1, 2, 3, 4, 5, 7],
                "work_hours": [11, 12, 13, 16, 17, 18, 19],
                "city": [598]
            },
            "new_zones": [1],
            "new_services": [1, 3]
        }

        client = APIClient()
        response = client.patch('/api/1.0/user/', data=data, format='json',
                                HTTP_AUTHORIZATION='Token {}'.format(token_jwt_1))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data.get('profile').get('work_days')[0],
                         _("Ensure this value is less than or equal to 6."))

    def test_user_professional_sent_invalid_work_hours(self):
        superuser = User.objects.get(username='aurora')
        token_jwt_1 = jwt_encode(superuser)

        data = {
            "first_name": "Aurora",
            "last_name": "Barrios",
            "profile": {
                "phone": "+34661661662",
                "picture": "",
                "type": "PRO",
                "iban_bank_account": "ES5221003179712200170953",
                "swift_bank_account": "CAGLESMMCOP",
                "documents": ["http://www.facebook.com/", "http://www.google.es"],
                "work_days": [1, 2, 3, 4, 5],
                "work_hours": [11, 12, 13, 16, 17, 18, 24],
                "city": [598]
            },
            "new_zones": [1],
            "new_services": [1, 3]
        }

        client = APIClient()
        response = client.patch('/api/1.0/user/', data=data, format='json',
                                HTTP_AUTHORIZATION='Token {}'.format(token_jwt_1))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data.get('profile').get('work_hours')[0],
                         _("Ensure this value is less than or equal to 23."))
