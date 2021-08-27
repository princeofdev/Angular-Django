from django.db import IntegrityError
from django.utils.translation import ugettext as _

from djstripe.models import Customer, Card
from rest_framework import status
from rest_framework.generics import ListCreateAPIView, DestroyAPIView
from rest_framework.response import Response
from stripe import CardError

from credit_cards.serializers import CardCreateSerializer, CardListSerializer
from kf.viewsets import MultipleSerializersViewSet


class CardViewSet(MultipleSerializersViewSet, ListCreateAPIView, DestroyAPIView):
    """
    post:
    Create a credit card for login user
    """
    queryset = Card.objects.all()
    list_serializer_class = CardListSerializer
    create_serializer_class = CardCreateSerializer

    def list(self, request, *args, **kwargs):
        user = self.request.user
        customer, created = Customer.get_or_create(user)
        cards = customer.sources.get_queryset()
        serializer = self.get_serializer(cards, many=True)

        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = self.request.user
        customer, created = Customer.get_or_create(user)
        try:
            customer.add_card(source=serializer.data, set_default=True)
        except CardError as e:
            return Response({e.code: e._message}, status=status.HTTP_400_BAD_REQUEST)
        except IntegrityError as e:
            return Response({"integrity_error": e.args[0]}, status=status.HTTP_400_BAD_REQUEST)

        return Response(data=_("Credit card added."), status=status.HTTP_201_CREATED)

    def perform_destroy(self, instance):
        user = self.request.user
        customer, created = Customer.get_or_create(user)
        user_cards = customer.sources.values_list('stripe_id', flat=True)
        if instance.stripe_id not in user_cards:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        if len(user_cards) == 1:
            return Response({"error": _("There must be one credit card at least.")}, status=status.HTTP_400_BAD_REQUEST)

        instance.remove()
        return Response(status=status.HTTP_204_NO_CONTENT)
