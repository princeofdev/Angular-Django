from rest_framework.generics import CreateAPIView, get_object_or_404
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK

from smsverification.client import BrokerClient
from smsverification.exceptions import InvalidCodeException
from smsverification.models import VerificationCode
from smsverification.serializers import RequestVerificationCodeSerializer, CodeVerificationSerializer
from smsverification.settings import MESSAGE_TEMPLATE


class RequestVerificationAPIView(CreateAPIView):
    """
    Sends a SMS with a verification code to the give phone number (if its correct)
    """
    queryset = VerificationCode.objects.all()
    serializer_class = RequestVerificationCodeSerializer
    permission_classes = ()

    def perform_create(self, serializer):
        verification_code = serializer.save()
        #client = BrokerClient()
        #client.send(verification_code.phone, MESSAGE_TEMPLATE.format(verification_code.code))
        return verification_code


class CodeVerificationAPIView(CreateAPIView):
    """
    Verify a verification code related with a phone number
    """
    permission_classes = ()
    serializer_class = CodeVerificationSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.save()

        verification_code = VerificationCode.objects.filter(phone=data.phone, code=data.code, verification_date=None).first()
        if not verification_code or verification_code.is_expired():
            raise InvalidCodeException()

        verification_code.verify()

        return Response({"code": "verified"}, status=HTTP_200_OK)
