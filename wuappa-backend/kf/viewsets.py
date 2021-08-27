# -*- coding: utf-8 -*-
from rest_framework.mixins import ListModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet


class MultipleSerializersViewSet(GenericViewSet):
    """
    A ViewSet that allows to define several serializers for the different actions.
    If not defined, the serializer_class is returned by default.
    """
    list_serializer_class = None
    create_serializer_class = None
    retrieve_serializer_class = None
    update_serializer_class = None
    partial_update_serializer_class = None
    destroy_serializer_class = None

    def get_serializer_class(self):
        if self.action == 'list' and self.list_serializer_class:
            return self.list_serializer_class
        elif self.action == 'create' and self.create_serializer_class:
            return self.create_serializer_class
        elif self.action == 'retrieve' and self.retrieve_serializer_class:
            return self.retrieve_serializer_class
        elif self.action == 'update' and self.update_serializer_class:
            return self.update_serializer_class
        elif self.action == 'partial_update' and self.partial_update_serializer_class:
            return self.partial_update_serializer_class
        elif self.action == 'destroy' and self.destroy_serializer_class:
            return self.destroy_serializer_class
        else:
            return self.serializer_class


class RetrieveAllModelMixin(GenericViewSet, ListModelMixin):
    def get_queryset(self):
        queryset = self.queryset
        if self.request.query_params.get('ids') is not None:
            try:
                list_ids = map(int, str(self.request.query_params.get('ids')).split(','))
            except:
                return queryset

            return queryset.filter(id__in=list_ids)

        return queryset

    def list(self, request, *args, **kwargs):
        if request.query_params.get('retrieveAll') is None:
            return super(RetrieveAllModelMixin, self).list(request, *args, **kwargs)
        else:
            queryset = self.filter_queryset(self.get_queryset()).values_list(request.query_params.get('retrieveAll'),
                                                                             flat=True)
        return Response(list(queryset))
