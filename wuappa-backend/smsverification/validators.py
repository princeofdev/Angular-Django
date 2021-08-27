import phonenumbers
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext as _
from phonenumbers import NumberParseException


def validate_phone_number(value):
    try:
        z = phonenumbers.parse(value, None)
    except NumberParseException as e:
        raise ValidationError(str(e))

    is_valid = phonenumbers.is_valid_number(z)
    if not is_valid:
        raise ValidationError(_("This phone number is not valid."))
