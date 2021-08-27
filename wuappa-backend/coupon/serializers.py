
from rest_framework import serializers

from coupon.models import Coupon


class CouponSerializer(serializers.ModelSerializer):

    class Meta:
        model = Coupon
        fields = '__all__'

    def partial_update(self, instance, validated_data):
        instance.redemption = validated_data.get('redemption')
        instance.valid = validated_data.get('valid')
        instance.save()
        return instance
