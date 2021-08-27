import warnings
from calendar import timegm
from datetime import datetime

from rest_framework_jwt.compat import get_username, get_username_field
from rest_framework_jwt.settings import api_settings


def jwt_payload_handler(user):
    username_field = get_username_field()
    username = get_username(user)

    warnings.warn(
        'The following fields will be removed in the future: '
        '`email` and `user_id`. ',
        DeprecationWarning
    )

    payload = {
        'user_id': user.pk,
        'email': user.email,
        'username': username,
        'exp': datetime.utcnow() + api_settings.JWT_EXPIRATION_DELTA
    }

    payload[username_field] = username

    # Include original issued at time for a brand new token,
    # to allow token refresh
    if api_settings.JWT_ALLOW_REFRESH:
        payload['orig_iat'] = timegm(
            datetime.utcnow().utctimetuple()
        )

    if api_settings.JWT_AUDIENCE is not None:
        payload['aud'] = api_settings.JWT_AUDIENCE

    if api_settings.JWT_ISSUER is not None:
        payload['iss'] = api_settings.JWT_ISSUER

    payload['phone'] = user.profile.phone
    payload['type'] = user.profile.type
    payload['picture'] = user.profile.picture
    payload['swift_bank_account'] = user.profile.swift_bank_account
    payload['iban_bank_account'] = user.profile.iban_bank_account
    payload['documents'] = user.profile.documents
    payload['first_name'] = user.first_name
    payload['last_name'] = user.last_name
    payload['account_name'] = user.profile.account_name
    payload['city'] = user.profile.city

    return payload
