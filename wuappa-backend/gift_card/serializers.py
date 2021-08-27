
from rest_framework import serializers
from django.utils.translation import ugettext as _
from gift_card.models import GiftCard


class GiftCardSerializer(serializers.ModelSerializer):

    class Meta:
        model = GiftCard
        fields = '__all__'

    def validate(self, data):
        request = self.context.get("request")
        data['buyer'] = request.user
        data['remaining_amount'] = request.data.get('amount_off')
        return data

    def partial_update(self, instance, validated_data):
        instance.remaining_amount = validated_data.get('amount_off') 
        instance.redemption = validated_data.get('redemption')
        instance.valid = validated_data.get('valid')
        instance.buyer = self.request.user
        instance.save()
        return instance

    # def create(self, validated_data):
    #    giftCard = GiftCard.objects.create(**validated_data)
    #    return giftCard;