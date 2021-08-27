# -*- coding: utf-8 -*-
import json

from django.conf import settings
from rest_framework import serializers

FIELDS_SELECTOR_QUERY_PARAM = getattr(settings, 'FIELDS_SELECTOR_QUERY_PARAM', 'fields')


class DynamicFieldsModelSerializer(serializers.ModelSerializer):
    """
    A ModelSerializer that takes an additional `query argument` argument that
    controls which fields should be displayed.
    """

    def __init__(self, *args, **kwargs):
        super(DynamicFieldsModelSerializer, self).__init__(*args, **kwargs)
        request = self.context.get('request')
        if request is not None:
            fields = request.query_params.get(FIELDS_SELECTOR_QUERY_PARAM)
            if fields:
                fields = fields.split(',')
                # Drop any fields that are not specified in the `fields` argument.
                allowed = set(fields)
                existing = set(self.fields.keys())
                for field_name in existing - allowed:
                    self.fields.pop(field_name)


class TrickField(serializers.Field):
    def to_internal_value(self, value):
        try:
            return json.loads(value) if isinstance(value, str) else value
        except ValueError:
            return {}

    def to_representation(self, value):
        try:
            return json.dumps(value) if isinstance(value, dict) else value
        except ValueError:
            return json.dumps({})
