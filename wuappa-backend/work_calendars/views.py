from rest_framework import status
from rest_framework.generics import ListCreateAPIView, get_object_or_404
from rest_framework.response import Response

from kf.viewsets import MultipleSerializersViewSet
from work_calendars.models import DayOff
from work_calendars.serializers import DayOffListSerializer, DayOffCreateSerializer


class DayOffViewSet(MultipleSerializersViewSet, ListCreateAPIView):
    """
    list:
    List days off for a professional login in app.

    post:
    Add a professional day off.

    delete:
    Delete a professional day off by date. Only can delete if user is the dayoff owner.
    """
    queryset = DayOff.objects.all()
    serializer_class = DayOffListSerializer
    list_serializer_class = DayOffListSerializer
    create_serializer_class = DayOffCreateSerializer

    def get_queryset(self):
        queryset = self.queryset
        return queryset.filter(professional=self.request.user)

    def destroy(self, request, pk):
        dayoff = get_object_or_404(DayOff, date=pk, professional=request.user)
        dayoff.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
