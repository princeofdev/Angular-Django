from django.contrib.auth.models import User
from django.utils.translation import ugettext as _
from rest_framework import serializers

from profiles.settings import PROFESSIONAL
from work_calendars.models import DayOff


class DayOffListSerializer(serializers.ModelSerializer):
    professional_email = serializers.SerializerMethodField()

    class Meta:
        model = DayOff
        fields = '__all__'

    def get_professional_email(self, obj):
        return obj.professional.email


class DayOffCreateSerializer(serializers.ModelSerializer):
    professional = serializers.PrimaryKeyRelatedField(read_only=True, default=serializers.CurrentUserDefault())

    class Meta:
        model = DayOff
        fields = '__all__'

    def validate(self, data):
        professional = data.get('professional')
        if professional.profile.type != PROFESSIONAL:
            raise serializers.ValidationError(_("User must be a professional."))
        return data
