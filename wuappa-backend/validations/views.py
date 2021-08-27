from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from validations.serializers import PhoneValidatorSerializer, EmailValidatorSerializer, BankAccountValidatorSerializer


class PhoneValidatorViewSet(GenericViewSet, CreateAPIView):
    """
    Verify if a phone number is valid
    """
    permission_classes = ()
    serializer_class = PhoneValidatorSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        return Response(data=serializer.data, status=status.HTTP_200_OK)


class EmailValidatorViewSet(GenericViewSet, CreateAPIView):
    """
    Verify if an email is valid and there is not another equal register in app
    """
    permission_classes = ()
    serializer_class = EmailValidatorSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        return Response(data=serializer.data, status=status.HTTP_200_OK)


class BankAccountValidatorViewSet(GenericViewSet, CreateAPIView):
    """
    Verify if iban and swift account code are valid
    """
    permission_classes = ()
    serializer_class = BankAccountValidatorSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        return Response(data=serializer.data, status=status.HTTP_200_OK)
