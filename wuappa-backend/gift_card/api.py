from rest_framework.generics import ListCreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.status import HTTP_200_OK, HTTP_404_NOT_FOUND
from django.utils.translation import ugettext as _

from gift_card.models import GiftCard
from gift_card.serializers import GiftCardSerializer


class GiftCardListAPI(ListCreateAPIView):
    """
    Listado de Gift Card por ID
    """

    queryset = GiftCard.objects.all()
    serializer_class = GiftCardSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, code):
        try:
            coupon = GiftCard.objects.get(code=code, valid=True)
            if coupon.used_by.filter(user=request.user).exists():
                return Response({"error": _('Gift Card has already been used')}, status=HTTP_404_NOT_FOUND)
            serializer = self.get_serializer(coupon)
            return Response(serializer.data, status=HTTP_200_OK)
        except GiftCard.DoesNotExist:
            return Response({"error": _('Gift Card does not exist')}, status=HTTP_404_NOT_FOUND)

    """
    def post(self, request, *args, **kwargs):
        try:
            user = request.user
            send_email_confirmation(request, user)
        except serializers.ValidationError:
            return Response({"error": "Email does not exists"}, status=HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": "There was an error sending the email"}, status=HTTP_400_BAD_REQUEST)

        return Response({"success": "Email sent correctly"}, status=HTTP_200_OK)
    """

    # def perform_create(self, serializer):
    #    instance = serializer.save();
    #    return Response({"error": _('Gift Card does not exist')}, status=status.HTTP_400_BAD_REQUEST)
    
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()
        return Response(data=_("Gift Card added."), status=status.HTTP_201_CREATED)
        #return instance
    