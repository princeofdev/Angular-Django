# -*- coding: utf-8 -*-
import base64, uuid
from django.core.files.base import ContentFile
from rest_framework import serializers


class Base64FileField(serializers.FileField):

    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:'):
            # base64 encoded image - decode
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]
            id = uuid.uuid4()
            data = ContentFile(base64.b64decode(imgstr), name = id.urn[9:] + '.' + ext)
        return super(Base64FileField, self).to_internal_value(data)

    def to_representation(self, value):
        return value
