# -*- coding: utf-8 -*-
from django.conf import settings
from django.core.files.storage import default_storage
from rest_framework.serializers import Serializer

from files.fields import Base64FileField


class File(object):
    pass


class FileSerializer(Serializer):

    file = Base64FileField()

    def create(self, validated_data):
        file = validated_data.get("file")
        path = default_storage.save(file.name, file)
        request = self.context.get("request")
        full_url = request.build_absolute_uri("{0}{1}".format(settings.MEDIA_URL, path)) if request else ""
        file = File()
        file.file = full_url
        return file
