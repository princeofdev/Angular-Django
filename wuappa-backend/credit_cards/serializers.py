from djstripe.models import Card
from rest_framework import serializers


class CardListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Card
        fields = '__all__'


class CardCreateSerializer(serializers.Serializer):
    object = serializers.CharField(default="card")  # Required
    exp_month = serializers.IntegerField(min_value=1, max_value=12)
    exp_year = serializers.IntegerField()
    number = serializers.CharField()
    currency = serializers.CharField(default="EUR")
    cvc = serializers.CharField()
    default_for_currency = serializers.BooleanField(default=False)
    name = serializers.CharField(max_length=255, required=False, allow_null=True, allow_blank=True)

    class Meta:
        model = Card
        fields = '__all__'
