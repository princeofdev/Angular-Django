# -*- coding: utf-8 -*-
from json import JSONDecodeError

import requests
from requests import RequestException
from simplejson import JSONDecodeError as SimpleJSONDecodeError

from smsverification.exceptions import SMSSendException
from smsverification.settings import BROKER_ENDPOINT, BROKER_PASSWORD, BROKER_USER, DEBUG_MODE, SENDER_ID
from smsverification.validators import validate_phone_number


class BrokerClient(object):

    def send(self, target, message):
        try:
            validate_phone_number(target)
            if DEBUG_MODE:
                return dict()
            r = requests.post(BROKER_ENDPOINT, data={
                'user': BROKER_USER,
                'pw': BROKER_PASSWORD,
                'snr': SENDER_ID,
                'dnr': target,
                'msg': message,
                'json': 1,
                'test': 1 if DEBUG_MODE else 0
            })
            r.raise_for_status()
            response = r.json()
            message_count = response.get("message-count", 0)
            messages = response.get("messages", list())
            message = messages[0] if len(messages) == 1 else dict()
            if message_count != 1 or message.get("status") != "OK" or message.get("dnr") != target:
                raise SMSSendException()
            return response
        except (RequestException, JSONDecodeError, SimpleJSONDecodeError):
            raise SMSSendException()
