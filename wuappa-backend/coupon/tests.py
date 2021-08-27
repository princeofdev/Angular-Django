from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from coupon.models import Coupon, UsedCoupon


class CouponsTests(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user_with_coupon = User.objects.create_user("batman", "bruce@waynecorp.com")
        self.user_without_coupon = User.objects.create_user("alfred", "alfred@waynecorp.com")
        self.valid_coupon = Coupon.objects.create(
            code="BATMAN", type="MON", amount_off=1
        )
        self.invalid_coupon = Coupon.objects.create(
            code="ALFRED", type="MON", amount_off=1, valid=False
        )
        UsedCoupon.objects.create(coupon=self.invalid_coupon, user=self.user_with_coupon)

    def test_user_is_not_authenticate(self):
        response = self.client.get("/api/1.0/coupon/{0}".format(self.valid_coupon.code))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_coupon_does_not_exist(self):
        self.client.force_authenticate(user=self.user_with_coupon)
        response = self.client.get("/api/1.0/coupon/DOES_NOT_EXIST")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_coupon_exist_and_is_valid(self):
        self.client.force_authenticate(user=self.user_with_coupon)
        response = self.client.get("/api/1.0/coupon/{0}".format(self.valid_coupon.code))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get("code"), self.valid_coupon.code)

    def test_coupon_exist_and_is_not_valid(self):
        self.client.force_authenticate(user=self.user_with_coupon)
        response = self.client.get("/api/1.0/coupon/{0}".format(self.invalid_coupon.code))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_coupon_exist_and_not_belongs_to_user(self):
        self.client.force_authenticate(user=self.user_without_coupon)
        response = self.client.get("/api/1.0/coupon/{0}".format(self.invalid_coupon.code))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
