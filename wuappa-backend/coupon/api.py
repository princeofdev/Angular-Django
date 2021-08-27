from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_404_NOT_FOUND
from django.utils.translation import ugettext as _

from coupon.models import Coupon
from coupon.serializers import CouponSerializer


class CouponListAPI(GenericAPIView):
    """
    Listado de Cupones por ID
    """

    queryset = Coupon.objects.all()
    serializer_class = CouponSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, code):
        try:
            coupon = Coupon.objects.get(code=code, valid=True)
            if coupon.used_by.filter(user=request.user).exists():
                return Response({"error": _('Coupon has already been used')}, status=HTTP_404_NOT_FOUND)
            serializer = self.get_serializer(coupon)
            return Response(serializer.data, status=HTTP_200_OK)
        except Coupon.DoesNotExist:
            return Response({"error": _('Coupon does not exist')}, status=HTTP_404_NOT_FOUND)
