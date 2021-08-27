from rest_framework import serializers

from smsverification.models import VerificationCode
from smsverification.validators import validate_phone_number


class RequestVerificationCodeSerializer(serializers.ModelSerializer):

    class Meta:
        model = VerificationCode
        fields = ('phone',)


class CodeVerificationSerializer(serializers.Serializer):

    phone = serializers.CharField(max_length=20, validators=[validate_phone_number])
    code = serializers.CharField(max_length=20)

    def create(self, validated_data):
        return VerificationCode(phone=validated_data.get("phone"), code=validated_data.get("code"))
