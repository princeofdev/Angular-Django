from django.contrib.auth.models import User
from django.utils.translation import ugettext as _
from django_iban.validators import IBANValidator, swift_bic_validator
from rest_framework import serializers

from smsverification.validators import validate_phone_number


class PhoneValidatorSerializer(serializers.Serializer):
    phone = serializers.CharField(max_length=20, validators=[validate_phone_number])


class EmailValidatorSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate(self, data):
        try:
            email = data.get('email')
            User.objects.get(email=email)
            raise serializers.ValidationError(_("Email already exist."))
        except User.DoesNotExist:
            return data


class BankAccountValidatorSerializer(serializers.Serializer):
    iban_bank_account = serializers.CharField()
    swift_bank_account = serializers.CharField()

    def validate_iban_bank_account(self, iban):
        iban_validator = IBANValidator()
        iban_validator.__call__(iban)
        return iban

    def validate_swift_bank_account(self, swift):
        swift_bic_validator(swift)
        return swift
