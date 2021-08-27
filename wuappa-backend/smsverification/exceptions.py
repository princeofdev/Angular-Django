from rest_framework.exceptions import APIException
from django.utils.translation import ugettext as _
from rest_framework.status import HTTP_502_BAD_GATEWAY, HTTP_400_BAD_REQUEST


class SMSSendException(APIException):
    status_code = HTTP_502_BAD_GATEWAY
    default_detail = _('There was a problem sending the SMS. Try again later.')
    default_code = 'broker_connection_error'


class InvalidCodeException(APIException):
    status_code = HTTP_400_BAD_REQUEST
    default_detail = _('Invalid code')
    default_code = 'invalid_code'
