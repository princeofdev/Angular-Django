import datetime

from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.translation import ugettext as _
from djmoney.money import Money
from djstripe.models import Customer, Card
from rest_framework import serializers
from rest_framework.fields import SerializerMethodField

from geo.models import WorkZone
from profiles.serializers import UserDetailsSerializer
from profiles.settings import FINAL, PROFESSIONAL
from services.models import Service, Category, CityServices, HireService, HireServiceService
from services.settings import PENDING, ACCEPT, COMPLETE
from coupon.models import Coupon


class CityServiceSerializer(serializers.ModelSerializer):
    city_name = serializers.SerializerMethodField()

    class Meta:
        model = CityServices
        fields = '__all__'

    def get_city_name(self, obj):
        return obj.city.name


class CategorySerializer(serializers.ModelSerializer):
    cities = CityServiceSerializer(source='get_cities', many=True)

    class Meta:
        model = Category
        exclude = ('name_en', 'name_fr')


class ServiceSerializer(serializers.ModelSerializer):
    cities = SerializerMethodField()

    class Meta:
        model = Service
        exclude = ('name_en', 'name_fr', 'description_en', 'description_fr', 'preparation_en', 'preparation_fr')

    def get_cities(self, obj):
        city_services = obj.city_services.all()
        zip = self.context.get('zip')
        if zip:
            workzone_cities = WorkZone.objects.filter(zip_codes__icontains=zip).values_list('city', flat=True)
            city_services = city_services.filter(city__in=workzone_cities)
        serializer = CityServiceSerializer(city_services, many=True)
        return serializer.data


class HireServiceSerializer(serializers.ModelSerializer):
    client = UserDetailsSerializer()
    professional = UserDetailsSerializer()

    class Meta:
        model = HireService
        fields = '__all__'
        depth = 1


class HireServiceDetailSerializer(serializers.ModelSerializer):
    client = UserDetailsSerializer()
    professional = UserDetailsSerializer()
    credit_card = serializers.SerializerMethodField()

    class Meta:
        model = HireService
        fields = '__all__'
        depth = 1

    def get_credit_card(self, obj):
        try:
            card = Card.objects.get(stripe_id=obj.credit_card)
            return {
                'brand': card.brand,
                'last4': card.last4,
                'exp_month': card.exp_month,
                'exp_year': card.exp_year
            }
        except Card.DoesNotExist:
            return dict()


class HireServiceCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = HireService
        fields = '__all__'

    def validate_coupon(self, value):
        try:
            request = self.context.get("request")
            if value is not None:
                coupon = Coupon.objects.get(valid=True, code=value)
                if coupon.used_by.filter(user=request.user).exists():
                    raise serializers.ValidationError(_("Coupon does not exist or is already used"))
            else:
                coupon = None
            return coupon
        except Coupon.DoesNotExist:
            raise serializers.ValidationError(_("Coupon does not exist or is already used"))

    def validate(self, data):
        request = self.context.get("request")
        services = request.data.get('services')
        if services is None:
            raise serializers.ValidationError({"services": _("This field is required.")})
        elif len(services) == 0:
            raise serializers.ValidationError({"services": _("This list may not be empty.")})

        data_services = list()
        for service in services:
            try:
                data_services.append(Service.objects.get(pk=service))
            except Service.DoesNotExist:
                raise serializers.ValidationError({"services":
                                                       _("Invalid pk \"%s\" - object does not exist.") % service})

        data['services'] = data_services

        client = data.get('client')
        if client.profile.type != FINAL:
            raise serializers.ValidationError(_("Client user must be a final client, not professional"))
        professional = data.get('professional')
        if professional:
            if professional.profile.type != PROFESSIONAL:
                raise serializers.ValidationError(_("Professional user must be a professional"))

        # Date validation
        service_datetime = datetime.datetime.combine(data.get('date'), data.get('time'))
        if service_datetime < datetime.datetime.now():
            raise serializers.ValidationError(_("The selected date and time is in the past."))
        # Not allow to hire services if only 2 hours before now
        diff_dates = service_datetime - datetime.datetime.now()
        total_mins = (diff_dates.days * 1440 + diff_dates.seconds / 60)
        if 0 <= total_mins <= 120:
            raise serializers.ValidationError(_("The selected date is not enough to hire services."))

        # Validate credit card for client
        customer, created = Customer.get_or_create(client)
        if created:
            raise serializers.ValidationError(_("Client just register in stripe. Not linked credit cards"))
        card = data.get('credit_card')
        cards = customer.sources.get_queryset().values_list('stripe_id', flat=True)
        if card not in cards:
            raise serializers.ValidationError(_("Credit card number not belongs to the client"))

        # Validate Total
        if not data.get('total'):
            raise serializers.ValidationError(_("Total amount_must_be_included"))

        # Total validation
        cities = WorkZone.objects.filter(zip_codes__icontains=data.get('zip_code')).values_list('city', flat=True)
        services_prices = CityServices.objects.filter(city__in=cities, service__in=data.get('services'))
        prices = dict()
        vat_applied = dict()
        currency = None
        for service_price in services_prices:
            if currency is None:
                currency = service_price.price.currency
            prices[service_price.service.pk] = service_price.price
            vat_applied[service_price.service.pk] = service_price.price * service_price.vat_percent / 100.0

        calc_price = 0
        vat_total = 0
        for service in data.get('services', list()):
            calc_price += prices.get(service.pk, 0)
            vat_total += vat_applied.get(service.pk, 0)

        total = data.get('total')
        coupon = data.get('coupon')
        if coupon:
            calc_price = coupon.calculate_discount(calc_price)
        if float(total) != float(calc_price):
            raise serializers.ValidationError(_("Invalid price"))

        data['vat'] = vat_total
        if type(total) is Money:
            data['net_total'] = total - vat_total
        else:
            data['net_total'] = Money(amount=total, currency=currency) - vat_total
        return data

    def create(self, validated_data):
        services_data = validated_data.pop('services')
        hire_service = HireService.objects.create(**validated_data)
        for service in services_data:
            HireServiceService.objects.create(service=service, hireservice=hire_service)
        return hire_service


class HireServiceUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = HireService
        fields = '__all__'

    def validate(self, data):
        card = data.get('credit_card')
        if card:
            client = self.instance.client
            if client != self.context.get('request').user:
                raise serializers.ValidationError(_("Only client for the hire services can update credit card"))
            if client.profile.type != FINAL:
                raise serializers.ValidationError(_("Client user must be a final client, not professional"))

            # Validate credit card for client
            customer, created = Customer.get_or_create(client)
            if created:
                raise serializers.ValidationError(_("Client just register in stripe. Not linked credit cards"))

            cards = customer.sources.get_queryset().values_list('stripe_id', flat=True)
            if card not in cards:
                raise serializers.ValidationError(_("Credit card number not belongs to the client"))
        return data


class ProfessionalAcceptSerializer(serializers.ModelSerializer):
    professional = serializers.PrimaryKeyRelatedField(read_only=True, default=serializers.CurrentUserDefault())
    accept = serializers.BooleanField(required=True)
    id = serializers.PrimaryKeyRelatedField(queryset=HireService.objects.filter(status=PENDING))

    class Meta:
        model = HireService
        fields = ('professional', 'accept', 'id')

    def validate(self, data):
        professional = data.get('professional')
        if professional.profile.type != PROFESSIONAL:
            raise serializers.ValidationError(_("User must be a professional."))
        return data


class ProfessionalCompleteSerializer(serializers.ModelSerializer):
    professional = serializers.PrimaryKeyRelatedField(read_only=True, default=serializers.CurrentUserDefault())
    complete = serializers.BooleanField(required=True)
    id = serializers.PrimaryKeyRelatedField(queryset=HireService.objects.filter(status=ACCEPT))

    class Meta:
        model = HireService
        fields = ('professional', 'complete', 'id')

    def validate(self, data):
        professional = data.get('professional')
        if professional.profile.type != PROFESSIONAL:
            raise serializers.ValidationError(_("User must be a professional."))
        hire_service = data.get('id')
        if professional != hire_service.professional:
            raise serializers.ValidationError(_("Only professional for the hire services can complete the service."))
        return data


class ClientReviewSerializer(serializers.ModelSerializer):
    client = serializers.PrimaryKeyRelatedField(read_only=True, default=serializers.CurrentUserDefault())
    rating = serializers.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)], required=True)
    review = serializers.CharField(max_length=None, required=True)
    review_date = serializers.DateField(read_only=True, default=datetime.date.today)
    id = serializers.PrimaryKeyRelatedField(queryset=HireService.objects.filter(status=COMPLETE))

    class Meta:
        model = HireService
        fields = ('client', 'rating', 'id', 'review', 'review_date')

    def validate(self, data):
        client = data.get('client')
        if client.profile.type != FINAL:
            raise serializers.ValidationError(_("User must be a final."))
        hire_service = data.get('id')
        if client != hire_service.client:
            raise serializers.ValidationError(_("Only client for the hire services can review the service."))
        return data


class ProfessionalAvailabilitySerializer(serializers.Serializer):
    services = serializers.ListField(child=serializers.PrimaryKeyRelatedField(queryset=Service.objects.all()),
                                     required=True)
    zip = serializers.CharField(max_length=10, required=True, allow_blank=False)
    date = serializers.DateField(required=True)
    time = serializers.TimeField(required=True)
