from django.test import override_settings, TestCase
from django.utils.translation import ugettext_lazy as _
from rest_framework import status
from rest_framework.test import APIClient


@override_settings(ROOT_URLCONF='wuappa.urls')
class TestFinalRegisterAPI(TestCase):
    fixtures = ['registration_fixtures.json']

    def test_signup_type_final_sent_all_data_ok(self):
        data = {
            "email": "prueba@gmail.com",
            "first_name": "Aurora",
            "last_name": "Barrios",
            "password1": "123456asd",
            "password2": "123456asd",
            "phone": "+34661661661",
            "picture": "http://www.facebook.com/",
            "documents": ["http://www.facebook.com/", "http://www.google.es"],
            "city": [598]
        }

        client = APIClient()
        response = client.post("/api/1.0/registration/", data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_signup_type_professional_sent_city_as_string(self):
        data = {
            "type": "PRO",
            "email": "prueba@gmail.com",
            "first_name": "Aurora",
            "last_name": "Barrios",
            "password1": "123456asd",
            "password2": "123456asd",
            "phone": "+34661661661",
            "picture": "http://www.facebook.com/",
            "documents": ["http://www.facebook.com/", "http://www.google.es"],
            "iban_bank_account": "ES5221003179712200170953",
            "swift_bank_account": "CAGLESMMCOP",
            "services": [1, 3],
            "work_zones": [1],
            "work_days": [1, 2, 3, 4, 5],
            "work_hours": [10, 11, 12, 13, 16, 15, 18],
            "city": "598"
        }

        client = APIClient()
        response = client.post("/api/1.0/registration/", data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_signup_type_final_documents_not_sent_ok(self):
        data = {
            "email": "prueba@gmail.com",
            "first_name": "aaa",
            "last_name": "bbb",
            "password1": "123456asd",
            "password2": "123456asd",
            "phone": "+34661661661",
            "picture": "http://www.facebook.com/",
            "city": [598]
        }

        client = APIClient()
        response = client.post("/api/1.0/registration/", data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_signup_type_final_documents_sent_empty_ok(self):
        data = {
            "email": "prueba@gmail.com",
            "first_name": "aaa",
            "last_name": "bbb",
            "password1": "123456asd",
            "password2": "123456asd",
            "phone": "+34661661661",
            "picture": "http://www.facebook.com/",
            "documents": [],
            "city": [598]
        }

        client = APIClient()
        response = client.post("/api/1.0/registration/", data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_signup_type_final_documents_sent_empty_city(self):
        data = {
            "email": "prueba@gmail.com",
            "first_name": "aaa",
            "last_name": "bbb",
            "password1": "123456asd",
            "password2": "123456asd",
            "phone": "+34661661661",
            "picture": "http://www.facebook.com/",
            "documents": [],
            "city": []
        }

        client = APIClient()
        response = client.post("/api/1.0/registration/", data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_signup_type_final_picture_not_sent_ok(self):
        data = {
            "email": "prueba@gmail.com",
            "first_name": "Aurora",
            "last_name": "Barrios",
            "password1": "123456asd",
            "password2": "123456asd",
            "phone": "+34661661661",
            "documents": ["http://www.facebook.com/", "http://www.google.es"],
            "city": [598]
        }

        client = APIClient()
        response = client.post("/api/1.0/registration/", data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_signup_type_final_picture_sent_empty_ok(self):
        data = {
            "email": "prueba@gmail.com",
            "first_name": "Aurora",
            "last_name": "Barrios",
            "password1": "123456asd",
            "password2": "123456asd",
            "phone": "+34661661661",
            "picture": "",
            "documents": ["http://www.facebook.com/", "http://www.google.es"],
            "city": [598]
        }

        client = APIClient()
        response = client.post("/api/1.0/registration/", data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_signup_type_final_picture_sent_city_ok(self):
        data = {
            "email": "prueba@gmail.com",
            "first_name": "Aurora",
            "last_name": "Barrios",
            "password1": "123456asd",
            "password2": "123456asd",
            "phone": "+34661661661",
            "picture": "",
            "documents": ["http://www.facebook.com/", "http://www.google.es"]
        }

        client = APIClient()
        response = client.post("/api/1.0/registration/", data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_signup_type_final_ko_email_not_sent(self):
        data = {
            "first_name": "Aurora",
            "last_name": "Barrios",
            "password1": "123456asd",
            "password2": "123456asd",
            "phone": "+34661661661",
            "picture": "http://www.facebook.com/",
            "documents": ["http://www.facebook.com/", "http://www.google.es"],
            "city": [598]
        }

        client = APIClient()
        response = client.post("/api/1.0/registration/", data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data.get('email')[0], _("This field is required."))

    def test_signup_type_final_ko_email_sent_null(self):
        data = {
            "email": "",
            "first_name": "Aurora",
            "last_name": "Barrios",
            "password1": "123456asd",
            "password2": "123456asd",
            "phone": "+34661661661",
            "picture": "http://www.facebook.com/",
            "documents": ["http://www.facebook.com/", "http://www.google.es"],
            "city": [598]
        }

        client = APIClient()
        response = client.post("/api/1.0/registration/", data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data.get('email')[0], _("This field may not be blank."))

    def test_signup_type_final_ko_email_invalid_format(self):
        data = {
            "email": "prueba",
            "first_name": "Aurora",
            "last_name": "Barrios",
            "password1": "123456asd",
            "password2": "123456asd",
            "phone": "+34661661661",
            "picture": "http://www.facebook.com/",
            "documents": ["http://www.facebook.com/", "http://www.google.es"],
            "city": [598]
        }

        client = APIClient()
        response = client.post("/api/1.0/registration/", data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data.get('email')[0], _("Enter a valid email address."))

    def test_signup_type_final_ko_email_already_exists_format(self):
        data = {
            "email": "aurora@kasfactory.net",
            "first_name": "Aurora",
            "last_name": "Barrios",
            "password1": "123456asd",
            "password2": "123456asd",
            "phone": "+34661661661",
            "picture": "http://www.facebook.com/",
            "documents": ["http://www.facebook.com/", "http://www.google.es"],
            "city": [598]
        }

        client = APIClient()
        response = client.post("/api/1.0/registration/", data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data.get('email')[0], _("A user is already registered with this e-mail address."))

    def test_signup_type_final_ko_first_name_not_sent(self):
        data = {
            "email": "prueba@gmail.com",
            "last_name": "Barrios",
            "password1": "123456asd",
            "password2": "123456asd",
            "phone": "+34661661661",
            "picture": "http://www.facebook.com/",
            "documents": ["http://www.facebook.com/", "http://www.google.es"],
            "city": [598]
        }

        client = APIClient()
        response = client.post("/api/1.0/registration/", data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data.get('first_name')[0], _("This field is required."))

    def test_signup_type_final_ko_first_name_sent_null(self):
        data = {
            "email": "prueba@gmail.com",
            "first_name": "",
            "last_name": "Barrios",
            "password1": "123456asd",
            "password2": "123456asd",
            "phone": "+34661661661",
            "picture": "http://www.facebook.com/",
            "documents": ["http://www.facebook.com/", "http://www.google.es"],
            "city": [598]
        }

        client = APIClient()
        response = client.post("/api/1.0/registration/", data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data.get('first_name')[0], _("This field may not be blank."))

    def test_signup_type_final_ko_last_name_not_sent(self):
        data = {
            "email": "prueba@gmail.com",
            "first_name": "Aurora",
            "password1": "123456asd",
            "password2": "123456asd",
            "phone": "+34661661661",
            "picture": "http://www.facebook.com/",
            "documents": ["http://www.facebook.com/", "http://www.google.es"],
            "city": [598]
        }

        client = APIClient()
        response = client.post("/api/1.0/registration/", data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data.get('last_name')[0], _("This field is required."))

    def test_signup_type_final_ko_last_name_sent_null(self):
        data = {
            "email": "prueba@gmail.com",
            "first_name": "Aurora",
            "last_name": "",
            "password1": "123456asd",
            "password2": "123456asd",
            "phone": "+34661661661",
            "picture": "http://www.facebook.com/",
            "documents": ["http://www.facebook.com/", "http://www.google.es"],
            "city": [598]
        }

        client = APIClient()
        response = client.post("/api/1.0/registration/", data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data.get('last_name')[0], _("This field may not be blank."))

    def test_signup_type_final_ko_password1_not_sent(self):
        data = {
            "email": "prueba@gmail.com",
            "first_name": "Aurora",
            "last_name": "Barrios",
            "password2": "123456asd",
            "phone": "+34661661661",
            "picture": "http://www.facebook.com/",
            "documents": ["http://www.facebook.com/", "http://www.google.es"],
            "city": [598]
        }

        client = APIClient()
        response = client.post("/api/1.0/registration/", data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data.get('password1')[0], _("This field is required."))

    def test_signup_type_final_ko_password1_sent_null(self):
        data = {
            "email": "prueba@gmail.com",
            "first_name": "Aurora",
            "last_name": "Barrios",
            "password1": "",
            "password2": "123456asd",
            "phone": "+34661661661",
            "picture": "http://www.facebook.com/",
            "documents": ["http://www.facebook.com/", "http://www.google.es"],
            "city": [598]
        }

        client = APIClient()
        response = client.post("/api/1.0/registration/", data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data.get('password1')[0], _("This field may not be blank."))

    def test_signup_type_final_ko_password_not_match_not_sent(self):
        data = {
            "email": "prueba@gmail.com",
            "first_name": "Aurora",
            "last_name": "Barrios",
            "password1": "123456asd1",
            "password2": "123456asd",
            "phone": "+34661661661",
            "picture": "http://www.facebook.com/",
            "documents": ["http://www.facebook.com/", "http://www.google.es"],
            "city": [598]
        }

        client = APIClient()
        response = client.post("/api/1.0/registration/", data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data.get('non_field_errors')[0], _("The two password fields didn't match."))

    def test_signup_type_final_ko_last_password_too_short_null(self):
        data = {
            "email": "prueba@gmail.com",
            "first_name": "Aurora",
            "last_name": "Barrios",
            "password1": "123",
            "password2": "123",
            "phone": "+34661661661",
            "picture": "http://www.facebook.com/",
            "documents": ["http://www.facebook.com/", "http://www.google.es"],
            "city": [598]
        }

        client = APIClient()
        response = client.post("/api/1.0/registration/", data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data.get('password1')[0], _("Password must be a minimum of 6 characters."))

    def test_signup_type_final_ko_phone_not_sent(self):
        data = {
            "email": "prueba@gmail.com",
            "first_name": "Aurora",
            "last_name": "Barrios",
            "password1": "123456asd",
            "password2": "123456asd",
            "picture": "http://www.facebook.com/",
            "documents": ["http://www.facebook.com/", "http://www.google.es"],
            "city": [598]
        }

        client = APIClient()
        response = client.post("/api/1.0/registration/", data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data.get('phone')[0], _("This field is required."))

    def test_signup_type_final_ko_phone_sent_null(self):
        data = {
            "email": "prueba@gmail.com",
            "first_name": "Aurora",
            "last_name": "Barrios",
            "password1": "123456asd",
            "password2": "123456asd",
            "phone": "",
            "picture": "http://www.facebook.com/",
            "documents": ["http://www.facebook.com/", "http://www.google.es"],
            "city": [598]
        }

        client = APIClient()
        response = client.post("/api/1.0/registration/", data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data.get('phone')[0], _("This field may not be blank."))

    def test_signup_type_final_ko_phone_invalid_format_region_not_sent(self):
        data = {
            "email": "prueba@gmail.com",
            "first_name": "Aurora",
            "last_name": "Barrios",
            "password1": "123456asd",
            "password2": "123456asd",
            "phone": "661661661",
            "picture": "http://www.facebook.com/",
            "documents": ["http://www.facebook.com/", "http://www.google.es"],
            "city": [598]
        }

        client = APIClient()
        response = client.post("/api/1.0/registration/", data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data.get('phone')[0], _("Missing or invalid default region"))

    def test_signup_type_final_ko_phone_invalid_format(self):
        data = {
            "email": "prueba@gmail.com",
            "first_name": "Aurora",
            "last_name": "Barrios",
            "password1": "123456asd",
            "password2": "123456asd",
            "phone": "+346616616611",
            "picture": "http://www.facebook.com/",
            "documents": ["http://www.facebook.com/", "http://www.google.es"],
            "city": [598]
        }

        client = APIClient()
        response = client.post("/api/1.0/registration/", data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data.get('phone')[0], _("This phone number is not valid."))

    def test_signup_type_final_ko_sent_invalid_city(self):
        data = {
            "email": "prueba@gmail.com",
            "first_name": "Aurora",
            "last_name": "Barrios",
            "password1": "123456asd",
            "password2": "123456asd",
            "phone": "+34661661661",
            "picture": "http://www.facebook.com/",
            "documents": ["http://www.facebook.com/", "http://www.google.es"],
            "city": [0]
        }

        client = APIClient()
        response = client.post("/api/1.0/registration/", data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data.get('city')[0], _("Invalid pk \"0\" - object does not exist."))

    def test_signup_type_final_ko_sent_invalid_city_format(self):
        data = {
            "email": "prueba@gmail.com",
            "first_name": "Aurora",
            "last_name": "Barrios",
            "password1": "123456asd",
            "password2": "123456asd",
            "phone": "+34661661661",
            "picture": "http://www.facebook.com/",
            "documents": ["http://www.facebook.com/", "http://www.google.es"],
            "city": ""
        }

        client = APIClient()
        response = client.post("/api/1.0/registration/", data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        print(response.data)
        self.assertEqual(response.data[0], 'Expected a list of items but got type \"str\".')


@override_settings(ROOT_URLCONF='wuappa.urls')
class TestProfessionalRegisterAPI(TestCase):
    fixtures = ['registration_fixtures.json']

    def test_signup_type_professional_sent_all_data(self):
        data = {
            "type": "PRO",
            "email": "prueba@gmail.com",
            "first_name": "Aurora",
            "last_name": "Barrios",
            "password1": "123456asd",
            "password2": "123456asd",
            "phone": "+34661661661",
            "picture": "http://www.facebook.com/",
            "documents": ["http://www.facebook.com/", "http://www.google.es"],
            "iban_bank_account": "ES5221003179712200170953",
            "swift_bank_account": "CAGLESMMCOP",
            "services": [1, 3],
            "work_zones": [1],
            "work_days": [1, 2, 3, 4, 5],
            "work_hours": [10, 11, 12, 13, 16, 15, 18],
            "city": [598]
        }

        client = APIClient()
        response = client.post("/api/1.0/registration/", data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_signup_type_professional_documents_not_sent_ko(self):
        data = {
            "type": "PRO",
            "email": "prueba@gmail.com",
            "first_name": "aaa",
            "last_name": "bbb",
            "password1": "123456asd",
            "password2": "123456asd",
            "phone": "+34661661661",
            "picture": "http://www.facebook.com/",
            "iban_bank_account": "ES5221003179712200170953",
            "swift_bank_account": "CAGLESMMCOP",
            "services": [1, 3],
            "work_zones": [1],
            "city": [598]
        }

        client = APIClient()
        response = client.post("/api/1.0/registration/", data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data.get('non_field_errors')[0], _("Must include one document at least"))

    def test_signup_type_professional_ko_city_sent_empty_ko(self):
        data = {
            "type": "PRO",
            "email": "prueba@gmail.com",
            "first_name": "Aurora",
            "last_name": "Barrios",
            "password1": "123456asd",
            "password2": "123456asd",
            "phone": "+34661661661",
            "picture": "http://www.facebook.com/",
            "documents": ["http://www.facebook.com/", "http://www.google.es"],
            "iban_bank_account": "ES5221003179712200170953",
            "swift_bank_account": "CAGLESMMCOP",
            "services": [1, 3],
            "work_zones": [1],
            "city": []
        }

        client = APIClient()
        response = client.post("/api/1.0/registration/", data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data.get('non_field_errors')[0], _("Must include one city"))

    def test_signup_type_professional_documents_sent_empty_ko(self):
        data = {
            "type": "PRO",
            "email": "prueba@gmail.com",
            "first_name": "aaa",
            "last_name": "bbb",
            "password1": "123456asd",
            "password2": "123456asd",
            "phone": "+34661661661",
            "picture": "http://www.facebook.com/",
            "documents": [],
            "iban_bank_account": "ES5221003179712200170953",
            "swift_bank_account": "CAGLESMMCOP",
            "services": [1, 3],
            "work_zones": [1],
            "city": [598]
        }

        client = APIClient()
        response = client.post("/api/1.0/registration/", data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data.get('non_field_errors')[0], _("Must include one document at least"))

    def test_signup_type_professional_picture_not_sent_ok(self):
        data = {
            "type": "PRO",
            "email": "prueba@gmail.com",
            "first_name": "Aurora",
            "last_name": "Barrios",
            "password1": "123456asd",
            "password2": "123456asd",
            "phone": "+34661661661",
            "documents": ["http://www.facebook.com/", "http://www.google.es"],
            "iban_bank_account": "ES5221003179712200170953",
            "swift_bank_account": "CAGLESMMCOP",
            "services": [1, 3],
            "work_zones": [1],
            "city": [598]
        }

        client = APIClient()
        response = client.post("/api/1.0/registration/", data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_signup_type_professional_picture_sent_empty_ok(self):
        data = {
            "type": "PRO",
            "email": "prueba@gmail.com",
            "first_name": "Aurora",
            "last_name": "Barrios",
            "password1": "123456asd",
            "password2": "123456asd",
            "phone": "+34661661661",
            "picture": "",
            "documents": ["http://www.facebook.com/", "http://www.google.es"],
            "iban_bank_account": "ES5221003179712200170953",
            "swift_bank_account": "CAGLESMMCOP",
            "services": [1, 3],
            "work_zones": [1],
            "city": [598]
        }

        client = APIClient()
        response = client.post("/api/1.0/registration/", data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_signup_type_professional_ko_email_not_sent(self):
        data = {
            "type": "PRO",
            "first_name": "Aurora",
            "last_name": "Barrios",
            "password1": "123456asd",
            "password2": "123456asd",
            "phone": "+34661661661",
            "picture": "http://www.facebook.com/",
            "documents": ["http://www.facebook.com/", "http://www.google.es"],
            "iban_bank_account": "ES5221003179712200170953",
            "swift_bank_account": "CAGLESMMCOP",
            "services": [1, 3],
            "work_zones": [1],
            "city": [598]
        }

        client = APIClient()
        response = client.post("/api/1.0/registration/", data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data.get('email')[0], _("This field is required."))

    def test_signup_type_professional_ko_email_sent_null(self):
        data = {
            "type": "PRO",
            "email": "",
            "first_name": "Aurora",
            "last_name": "Barrios",
            "password1": "123456asd",
            "password2": "123456asd",
            "phone": "+34661661661",
            "picture": "http://www.facebook.com/",
            "documents": ["http://www.facebook.com/", "http://www.google.es"],
            "iban_bank_account": "ES5221003179712200170953",
            "swift_bank_account": "CAGLESMMCOP",
            "services": [1, 3],
            "work_zones": [1],
            "city": [598]
        }

        client = APIClient()
        response = client.post("/api/1.0/registration/", data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data.get('email')[0], _("This field may not be blank."))

    def test_signup_type_professional_ko_email_invalid_format(self):
        data = {
            "type": "PRO",
            "email": "prueba",
            "first_name": "Aurora",
            "last_name": "Barrios",
            "password1": "123456asd",
            "password2": "123456asd",
            "phone": "+34661661661",
            "picture": "http://www.facebook.com/",
            "documents": ["http://www.facebook.com/", "http://www.google.es"],
            "iban_bank_account": "ES5221003179712200170953",
            "swift_bank_account": "CAGLESMMCOP",
            "services": [1, 3],
            "work_zones": [1],
            "city": [598]
        }

        client = APIClient()
        response = client.post("/api/1.0/registration/", data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data.get('email')[0], _("Enter a valid email address."))

    def test_signup_type_professional_ko_email_already_exists_format(self):
        data = {
            "type": "PRO",
            "email": "aurora@kasfactory.net",
            "first_name": "Aurora",
            "last_name": "Barrios",
            "password1": "123456asd",
            "password2": "123456asd",
            "phone": "+34661661661",
            "picture": "http://www.facebook.com/",
            "documents": ["http://www.facebook.com/", "http://www.google.es"],
            "iban_bank_account": "ES5221003179712200170953",
            "swift_bank_account": "CAGLESMMCOP",
            "services": [1, 3],
            "work_zones": [1],
            "city": [598]
        }

        client = APIClient()
        response = client.post("/api/1.0/registration/", data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data.get('email')[0], _("A user is already registered with this e-mail address."))

    def test_signup_type_professional_ko_first_name_not_sent(self):
        data = {
            "type": "PRO",
            "email": "prueba@gmail.com",
            "last_name": "Barrios",
            "password1": "123456asd",
            "password2": "123456asd",
            "phone": "+34661661661",
            "picture": "http://www.facebook.com/",
            "documents": ["http://www.facebook.com/", "http://www.google.es"],
            "iban_bank_account": "ES5221003179712200170953",
            "swift_bank_account": "CAGLESMMCOP",
            "services": [1, 3],
            "work_zones": [1],
            "city": [598]
        }

        client = APIClient()
        response = client.post("/api/1.0/registration/", data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data.get('first_name')[0], _("This field is required."))

    def test_signup_type_professional_ko_first_name_sent_null(self):
        data = {
            "type": "PRO",
            "email": "prueba@gmail.com",
            "first_name": "",
            "last_name": "Barrios",
            "password1": "123456asd",
            "password2": "123456asd",
            "phone": "+34661661661",
            "picture": "http://www.facebook.com/",
            "documents": ["http://www.facebook.com/", "http://www.google.es"],
            "iban_bank_account": "ES5221003179712200170953",
            "swift_bank_account": "CAGLESMMCOP",
            "services": [1, 3],
            "work_zones": [1],
            "city": [598]
        }

        client = APIClient()
        response = client.post("/api/1.0/registration/", data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data.get('first_name')[0], _("This field may not be blank."))

    def test_signup_type_professional_ko_last_name_not_sent(self):
        data = {
            "type": "PRO",
            "email": "prueba@gmail.com",
            "first_name": "Aurora",
            "password1": "123456asd",
            "password2": "123456asd",
            "phone": "+34661661661",
            "picture": "http://www.facebook.com/",
            "documents": ["http://www.facebook.com/", "http://www.google.es"],
            "iban_bank_account": "ES5221003179712200170953",
            "swift_bank_account": "CAGLESMMCOP",
            "services": [1, 3],
            "work_zones": [1],
            "city": [598]
        }

        client = APIClient()
        response = client.post("/api/1.0/registration/", data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data.get('last_name')[0], _("This field is required."))

    def test_signup_type_professional_ko_last_name_sent_null(self):
        data = {
            "type": "PRO",
            "email": "prueba@gmail.com",
            "first_name": "Aurora",
            "last_name": "",
            "password1": "123456asd",
            "password2": "123456asd",
            "phone": "+34661661661",
            "picture": "http://www.facebook.com/",
            "documents": ["http://www.facebook.com/", "http://www.google.es"],
            "iban_bank_account": "ES5221003179712200170953",
            "swift_bank_account": "CAGLESMMCOP",
            "services": [1, 3],
            "work_zones": [1],
            "city": [598]
        }

        client = APIClient()
        response = client.post("/api/1.0/registration/", data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data.get('last_name')[0], _("This field may not be blank."))

    def test_signup_type_professional_ko_password1_not_sent(self):
        data = {
            "type": "PRO",
            "email": "prueba@gmail.com",
            "first_name": "Aurora",
            "last_name": "Barrios",
            "password2": "123456asd",
            "phone": "+34661661661",
            "picture": "http://www.facebook.com/",
            "documents": ["http://www.facebook.com/", "http://www.google.es"],
            "iban_bank_account": "ES5221003179712200170953",
            "swift_bank_account": "CAGLESMMCOP",
            "services": [1, 3],
            "work_zones": [1],
            "city": [598]
        }

        client = APIClient()
        response = client.post("/api/1.0/registration/", data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data.get('password1')[0], _("This field is required."))

    def test_signup_type_professional_ko_password1_sent_null(self):
        data = {
            "type": "PRO",
            "email": "prueba@gmail.com",
            "first_name": "Aurora",
            "last_name": "Barrios",
            "password1": "",
            "password2": "123456asd",
            "phone": "+34661661661",
            "picture": "http://www.facebook.com/",
            "documents": ["http://www.facebook.com/", "http://www.google.es"],
            "iban_bank_account": "ES5221003179712200170953",
            "swift_bank_account": "CAGLESMMCOP",
            "services": [1, 3],
            "work_zones": [1],
            "city": [598]
        }

        client = APIClient()
        response = client.post("/api/1.0/registration/", data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data.get('password1')[0], _("This field may not be blank."))

    def test_signup_type_professional_ko_password_not_match_not_sent(self):
        data = {
            "type": "PRO",
            "email": "prueba@gmail.com",
            "first_name": "Aurora",
            "last_name": "Barrios",
            "password1": "123456asd1",
            "password2": "123456asd",
            "phone": "+34661661661",
            "picture": "http://www.facebook.com/",
            "documents": ["http://www.facebook.com/", "http://www.google.es"],
            "city": [598]
        }

        client = APIClient()
        response = client.post("/api/1.0/registration/", data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data.get('non_field_errors')[0], _("The two password fields didn't match."))

    def test_signup_type_professional_ko_last_password_too_short_null(self):
        data = {
            "type": "PRO",
            "email": "prueba@gmail.com",
            "first_name": "Aurora",
            "last_name": "Barrios",
            "password1": "123",
            "password2": "123",
            "phone": "+34661661661",
            "picture": "http://www.facebook.com/",
            "documents": ["http://www.facebook.com/", "http://www.google.es"],
            "iban_bank_account": "ES5221003179712200170953",
            "swift_bank_account": "CAGLESMMCOP",
            "services": [1, 3],
            "work_zones": [1],
            "city": [598]
        }

        client = APIClient()
        response = client.post("/api/1.0/registration/", data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data.get('password1')[0], _("Password must be a minimum of 6 characters."))

    def test_signup_type_professional_ko_phone_not_sent(self):
        data = {
            "type": "PRO",
            "email": "prueba@gmail.com",
            "first_name": "Aurora",
            "last_name": "Barrios",
            "password1": "123456asd",
            "password2": "123456asd",
            "picture": "http://www.facebook.com/",
            "documents": ["http://www.facebook.com/", "http://www.google.es"],
            "iban_bank_account": "ES5221003179712200170953",
            "swift_bank_account": "CAGLESMMCOP",
            "services": [1, 3],
            "work_zones": [1],
            "city": [598]
        }

        client = APIClient()
        response = client.post("/api/1.0/registration/", data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data.get('phone')[0], _("This field is required."))

    def test_signup_type_professional_ko_phone_sent_null(self):
        data = {
            "type": "PRO",
            "email": "prueba@gmail.com",
            "first_name": "Aurora",
            "last_name": "Barrios",
            "password1": "123456asd",
            "password2": "123456asd",
            "phone": "",
            "picture": "http://www.facebook.com/",
            "documents": ["http://www.facebook.com/", "http://www.google.es"],
            "iban_bank_account": "ES5221003179712200170953",
            "swift_bank_account": "CAGLESMMCOP",
            "services": [1, 3],
            "work_zones": [1],
            "city": [598]
        }

        client = APIClient()
        response = client.post("/api/1.0/registration/", data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data.get('phone')[0], _("This field may not be blank."))

    def test_signup_type_professional_ko_phone_invalid_format_region_not_sent(self):
        data = {
            "type": "PRO",
            "email": "prueba@gmail.com",
            "first_name": "Aurora",
            "last_name": "Barrios",
            "password1": "123456asd",
            "password2": "123456asd",
            "phone": "661661661",
            "picture": "http://www.facebook.com/",
            "documents": ["http://www.facebook.com/", "http://www.google.es"],
            "iban_bank_account": "ES5221003179712200170953",
            "swift_bank_account": "CAGLESMMCOP",
            "services": [1, 3],
            "work_zones": [1],
            "city": [598]
        }

        client = APIClient()
        response = client.post("/api/1.0/registration/", data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data.get('phone')[0], _("Missing or invalid default region"))

    def test_signup_type_professional_ko_phone_invalid_format(self):
        data = {
            "type": "PRO",
            "email": "prueba@gmail.com",
            "first_name": "Aurora",
            "last_name": "Barrios",
            "password1": "123456asd",
            "password2": "123456asd",
            "phone": "+346616616611",
            "picture": "http://www.facebook.com/",
            "documents": ["http://www.facebook.com/", "http://www.google.es"],
            "iban_bank_account": "ES5221003179712200170953",
            "swift_bank_account": "CAGLESMMCOP",
            "services": [1, 3],
            "work_zones": [1],
            "city": [598]
        }

        client = APIClient()
        response = client.post("/api/1.0/registration/", data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data.get('phone')[0], _("This phone number is not valid."))

    def test_signup_type_professional_ko_city_invalid_format(self):
        data = {
            "type": "PRO",
            "email": "prueba@gmail.com",
            "first_name": "Aurora",
            "last_name": "Barrios",
            "password1": "123456asd",
            "password2": "123456asd",
            "phone": "+34661661661",
            "picture": "http://www.facebook.com/",
            "documents": ["http://www.facebook.com/", "http://www.google.es"],
            "iban_bank_account": "ES5221003179712200170953",
            "swift_bank_account": "CAGLESMMCOP",
            "services": [1, 3],
            "work_zones": [1],
            "city": ""
        }

        client = APIClient()
        response = client.post("/api/1.0/registration/", data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data[0], _("Expected a list of items but got type \"str\"."))

    def test_signup_type_professional_ko_city_invalid(self):
        data = {
            "type": "PRO",
            "email": "prueba@gmail.com",
            "first_name": "Aurora",
            "last_name": "Barrios",
            "password1": "123456asd",
            "password2": "123456asd",
            "phone": "+34661661661",
            "picture": "http://www.facebook.com/",
            "documents": ["http://www.facebook.com/", "http://www.google.es"],
            "iban_bank_account": "ES5221003179712200170953",
            "swift_bank_account": "CAGLESMMCOP",
            "services": [1, 3],
            "work_zones": [1],
            "city": [0]
        }

        client = APIClient()
        response = client.post("/api/1.0/registration/", data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data.get('city')[0], _("Invalid pk \"0\" - object does not exist."))

    def test_signup_type_professional_ko_invalid_iban_not_sent(self):
        data = {
            "type": "PRO",
            "email": "prueba@gmail.com",
            "first_name": "Aurora",
            "last_name": "Barrios",
            "password1": "123456asd",
            "password2": "123456asd",
            "phone": "+34661661661",
            "picture": "http://www.facebook.com/",
            "documents": ["http://www.facebook.com/", "http://www.google.es"],
            "swift_bank_account": "CAGLESMMCOP",
            "services": [1, 3],
            "work_zones": [1],
            "city": [598]
        }

        client = APIClient()
        response = client.post("/api/1.0/registration/", data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data.get('non_field_errors')[0], _("Must include iban and swift account number."))

    def test_signup_type_professional_ko_invalid_iban(self):
        data = {
            "type": "PRO",
            "email": "prueba@gmail.com",
            "first_name": "Aurora",
            "last_name": "Barrios",
            "password1": "123456asd",
            "password2": "123456asd",
            "phone": "+34661661661",
            "picture": "http://www.facebook.com/",
            "documents": ["http://www.facebook.com/", "http://www.google.es"],
            "iban_bank_account": "ES52210031797122001709531",
            "swift_bank_account": "CAGLESMMCOP",
            "services": [1, 3],
            "work_zones": [1],
            "city": [598]
        }

        client = APIClient()
        response = client.post("/api/1.0/registration/", data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data.get('iban_bank_account')[0], _("ES IBANs must contain 24 characters."))

    def test_signup_type_professional_invalid_swift_not_sent(self):
        data = {
            "type": "PRO",
            "email": "prueba@gmail.com",
            "first_name": "Aurora",
            "last_name": "Barrios",
            "password1": "123456asd",
            "password2": "123456asd",
            "phone": "+34661661661",
            "picture": "http://www.facebook.com/",
            "documents": ["http://www.facebook.com/", "http://www.google.es"],
            "iban_bank_account": "ES5221003179712200170953",
            "services": [1, 3],
            "work_zones": [1],
            "city": [598]
        }

        client = APIClient()
        response = client.post("/api/1.0/registration/", data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data.get('non_field_errors')[0], _("Must include iban and swift account number."))

    def test_signup_type_professional_ko_invalid_swift(self):
        data = {
            "type": "PRO",
            "email": "prueba@gmail.com",
            "first_name": "Aurora",
            "last_name": "Barrios",
            "password1": "123456asd",
            "password2": "123456asd",
            "phone": "+34661661661",
            "picture": "http://www.facebook.com/",
            "documents": ["http://www.facebook.com/", "http://www.google.es"],
            "iban_bank_account": "ES5221003179712200170953",
            "swift_bank_account": "CAGLESMMCOPA",
            "services": [1, 3],
            "work_zones": [1],
            "city": [598]
        }

        client = APIClient()
        response = client.post("/api/1.0/registration/", data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data.get('swift_bank_account')[0],
                         _("A SWIFT-BIC is either 8 or 11 characters long."))

    def test_signup_type_professional_ko_invalid_iban_swift_not_sent(self):
        data = {
            "type": "PRO",
            "email": "prueba@gmail.com",
            "first_name": "Aurora",
            "last_name": "Barrios",
            "password1": "123456asd",
            "password2": "123456asd",
            "phone": "+34661661661",
            "picture": "http://www.facebook.com/",
            "documents": ["http://www.facebook.com/", "http://www.google.es"],
            "services": [1, 3],
            "work_zones": [1],
            "city": [598]
        }

        client = APIClient()
        response = client.post("/api/1.0/registration/", data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data.get('non_field_errors')[0], _("Must include iban and swift account number."))

    def test_signup_type_professional_ko_phone_invalid_iban_swift_sent_null(self):
        data = {
            "type": "PRO",
            "email": "prueba@gmail.com",
            "first_name": "Aurora",
            "last_name": "Barrios",
            "password1": "123456asd",
            "password2": "123456asd",
            "phone": "+34661661661",
            "picture": "http://www.facebook.com/",
            "documents": ["http://www.facebook.com/", "http://www.google.es"],
            "iban_bank_account": "",
            "swift_bank_account": "",
            "services": [1, 3],
            "work_zones": [1],
            "city": [598]
        }

        client = APIClient()
        response = client.post("/api/1.0/registration/", data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data.get('non_field_errors')[0],
                         _("Must include iban and swift account number."))

    def test_signup_type_professional_ko_service_not_sent(self):
        data = {
            "type": "PRO",
            "email": "prueba@gmail.com",
            "first_name": "Aurora",
            "last_name": "Barrios",
            "password1": "123456asd",
            "password2": "123456asd",
            "phone": "+34661661661",
            "picture": "http://www.facebook.com/",
            "documents": ["http://www.facebook.com/", "http://www.google.es"],
            "iban_bank_account": "ES5221003179712200170953",
            "swift_bank_account": "CAGLESMMCOP",
            "work_zones": [1],
            "city": [598]
        }

        client = APIClient()
        response = client.post("/api/1.0/registration/", data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data.get('non_field_errors')[0], _("Must include one services at least"))

    def test_signup_type_professional_ko_service_sent_null(self):
        data = {
            "type": "PRO",
            "email": "prueba@gmail.com",
            "first_name": "Aurora",
            "last_name": "Barrios",
            "password1": "123456asd",
            "password2": "123456asd",
            "phone": "+34661661661",
            "picture": "http://www.facebook.com/",
            "documents": ["http://www.facebook.com/", "http://www.google.es"],
            "iban_bank_account": "ES5221003179712200170953",
            "swift_bank_account": "CAGLESMMCOP",
            "services": [],
            "work_zones": [1],
            "city": [598]
        }

        client = APIClient()
        response = client.post("/api/1.0/registration/", data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data.get('non_field_errors')[0], _("Must include one services at least"))

    def test_signup_type_professional_ko_invalid_services(self):
        data = {
            "type": "PRO",
            "email": "prueba@gmail.com",
            "first_name": "Aurora",
            "last_name": "Barrios",
            "password1": "123456asd",
            "password2": "123456asd",
            "phone": "+34661661661",
            "picture": "http://www.facebook.com/",
            "documents": ["http://www.facebook.com/", "http://www.google.es"],
            "iban_bank_account": "ES5221003179712200170953",
            "swift_bank_account": "CAGLESMMCOP",
            "services": [1, 3, 0],
            "work_zones": [1],
            "city": [598]
        }

        client = APIClient()
        response = client.post("/api/1.0/registration/", data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data.get('services')[0], _("Invalid pk \"0\" - object does not exist."))

    def test_signup_type_professional_ko_work_zones_not_sent(self):
        data = {
            "type": "PRO",
            "email": "prueba@gmail.com",
            "first_name": "Aurora",
            "last_name": "Barrios",
            "password1": "123456asd",
            "password2": "123456asd",
            "phone": "+34661661661",
            "picture": "http://www.facebook.com/",
            "documents": ["http://www.facebook.com/", "http://www.google.es"],
            "iban_bank_account": "ES5221003179712200170953",
            "swift_bank_account": "CAGLESMMCOP",
            "services": [1, 3],
            "city": [598]
        }

        client = APIClient()
        response = client.post("/api/1.0/registration/", data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data.get('non_field_errors')[0], _("Must include one work_zones at least"))

    def test_signup_type_professional_ko_work_zones_sent_null(self):
        data = {
            "type": "PRO",
            "email": "prueba@gmail.com",
            "first_name": "Aurora",
            "last_name": "Barrios",
            "password1": "123456asd",
            "password2": "123456asd",
            "phone": "+34661661661",
            "picture": "http://www.facebook.com/",
            "documents": ["http://www.facebook.com/", "http://www.google.es"],
            "iban_bank_account": "ES5221003179712200170953",
            "swift_bank_account": "CAGLESMMCOP",
            "services": [1, 3],
            "work_zones": [],
            "city": [598]
        }

        client = APIClient()
        response = client.post("/api/1.0/registration/", data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data.get('non_field_errors')[0], _("Must include one work_zones at least"))

    def test_signup_type_professional_ko_invalid_work_zones(self):
        data = {
            "type": "PRO",
            "email": "prueba@gmail.com",
            "first_name": "Aurora",
            "last_name": "Barrios",
            "password1": "123456asd",
            "password2": "123456asd",
            "phone": "+34661661661",
            "picture": "http://www.facebook.com/",
            "documents": ["http://www.facebook.com/", "http://www.google.es"],
            "iban_bank_account": "ES5221003179712200170953",
            "swift_bank_account": "CAGLESMMCOP",
            "services": [1, 3],
            "work_zones": [1, 0],
            "work_days": [1, 2, 3, 4, 5],
            "work_hours": [10, 11, 12, 13, 16, 15, 18],
            "city": [598]
        }

        client = APIClient()
        response = client.post("/api/1.0/registration/", data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data.get('work_zones')[0], _("Invalid pk \"0\" - object does not exist."))

    def test_signup_type_professional_ko_invalid_work_days(self):
        data = {
            "type": "PRO",
            "email": "prueba@gmail.com",
            "first_name": "Aurora",
            "last_name": "Barrios",
            "password1": "123456asd",
            "password2": "123456asd",
            "phone": "+34661661661",
            "picture": "http://www.facebook.com/",
            "documents": ["http://www.facebook.com/", "http://www.google.es"],
            "iban_bank_account": "ES5221003179712200170953",
            "swift_bank_account": "CAGLESMMCOP",
            "services": [1, 3],
            "work_zones": [1],
            "work_days": [1, 2, 3, 4, 5, 7],
            "work_hours": [10, 11, 12, 13, 16, 15, 18],
            "city": [598]
        }

        client = APIClient()
        response = client.post("/api/1.0/registration/", data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data.get('work_days')[0], _("Ensure this value is less than or equal to 6."))

    def test_signup_type_professional_ko_invalid_work_hours(self):
        data = {
            "type": "PRO",
            "email": "prueba@gmail.com",
            "first_name": "Aurora",
            "last_name": "Barrios",
            "password1": "123456asd",
            "password2": "123456asd",
            "phone": "+34661661661",
            "picture": "http://www.facebook.com/",
            "documents": ["http://www.facebook.com/", "http://www.google.es"],
            "iban_bank_account": "ES5221003179712200170953",
            "swift_bank_account": "CAGLESMMCOP",
            "services": [1, 3],
            "work_zones": [1],
            "work_days": [1, 2, 3, 4, 5],
            "work_hours": [10, 11, 12, 13, 16, 15, 18, 34],
            "city": [598]
        }

        client = APIClient()
        response = client.post("/api/1.0/registration/", data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data.get('work_hours')[0], _("Ensure this value is less than or equal to 23."))
