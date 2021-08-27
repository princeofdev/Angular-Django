from rest_framework import pagination
from rest_framework.response import Response
from django.conf import settings


class LinkHeaderPaginator(pagination.PageNumberPagination):
    page_size = settings.PAGE_SIZE

    def get_paginated_response(self, data):
        headers = dict()
        next_url = self.get_next_link()
        previous_url = self.get_previous_link()
        if next_url:
            headers["X-Next"] = next_url
        if previous_url:
            headers["X-Prev"] = previous_url
        return Response(data, headers=headers)
