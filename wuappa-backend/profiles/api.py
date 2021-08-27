from allauth.account.utils import send_email_confirmation
from django.contrib.auth.models import User
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_404_NOT_FOUND, HTTP_400_BAD_REQUEST


class ResendVerificationView(GenericAPIView):
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):

        try:
            user = User.objects.get(email=request.data.get('email'))
            send_email_confirmation(request, user)
        except serializers.ValidationError:
            return Response({"error": "Email does not exists"}, status=HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": "There was an error sending the email"}, status=HTTP_400_BAD_REQUEST)

        return Response({"success": "Email sent correctly"}, status=HTTP_200_OK)
