import phonenumbers
from allauth.account import app_settings as allauth_settings
from allauth.account.adapter import get_adapter
from allauth.account.utils import setup_user_email
from allauth.utils import email_address_exists
from constance import config
from django.conf import settings
from django.core.mail import mail_managers
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.translation import ugettext as _
from django_iban.validators import IBANValidator, swift_bic_validator
from phonenumbers import NumberParseException
from rest_auth.serializers import UserModel, PasswordResetSerializer
from rest_framework import serializers

from geo.models import WorkZone, City
from profiles.models import Profile, UserWorkZone
from profiles.settings import PROFILE_TYPE, FINAL, PROFESSIONAL
from profiles.utils import ProfileOperator, ServicesOperator, WorZonesOperator
from services.models import Service


class CustomCityField(serializers.PrimaryKeyRelatedField):

    def to_internal_value(self, data):
        if isinstance(data,str):
            data = [int(data)]
        super(CustomCityField, self).to_internal_value(data)


class CustomRegisterSerializer(serializers.Serializer):
    email = serializers.EmailField(required=allauth_settings.EMAIL_REQUIRED)
    first_name = serializers.CharField(required=True, write_only=True)
    last_name = serializers.CharField(required=True, write_only=True)
    password1 = serializers.CharField(required=True, write_only=True)
    password2 = serializers.CharField(required=True, write_only=True)
    phone = serializers.CharField(required=True, write_only=True)
    picture = serializers.URLField(required=False, allow_null=True, allow_blank=True)
    type = serializers.ChoiceField(choices=PROFILE_TYPE, default=FINAL, write_only=True)
    account_name = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    iban_bank_account = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    swift_bank_account = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    documents = serializers.ListField(child=serializers.URLField(), required=False, allow_null=True)
    work_days = serializers.ListField(child=serializers.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(6)]), required=False, allow_null=True)
    work_hours = serializers.ListField(child=serializers.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(23)]), required=False, allow_null=True)
    services = serializers.ListField(child=serializers.PrimaryKeyRelatedField(queryset=Service.objects.all()),
                                     required=False, allow_null=True)
    work_zones = serializers.ListField(child=serializers.PrimaryKeyRelatedField(queryset=WorkZone.objects.all()),
                                       required=False, allow_null=True)
    city = serializers.ListField(child=serializers.PrimaryKeyRelatedField(queryset=City.objects.all()),
                                 required=False, allow_null=True)
    language = serializers.CharField(required=False, allow_null=True, allow_blank=True)


    def is_valid(self, raise_exception):
        city = self.initial_data.get('city')
        if isinstance(city, str):
            if city:
                city = [int(city)]
            else:
                raise serializers.ValidationError(_("Expected a list of items but got type \"str\"."))
        self.initial_data['city'] = city
        super(CustomRegisterSerializer, self).is_valid(raise_exception)

    def validate_email(self, email):
        email = get_adapter().clean_email(email)
        if allauth_settings.UNIQUE_EMAIL:
            if email and email_address_exists(email):
                raise serializers.ValidationError(
                    _("A user is already registered with this e-mail address."))
        return email

    def validate_password1(self, password):
        return get_adapter().clean_password(password)

    def validate_phone(self, phone):
        try:
            z = phonenumbers.parse(phone, None)
            is_valid = phonenumbers.is_valid_number(z)
            if not is_valid:
                raise serializers.ValidationError(_("This phone number is not valid."))
        except NumberParseException:
            raise serializers.ValidationError(_("Missing or invalid default region"))
        except:
            raise serializers.ValidationError(_("This phone number is not valid."))
        return phone

    def validate_iban_bank_account(self, iban):
        if iban:
            iban_validator = IBANValidator()
            iban_validator.__call__(iban)
        return iban

    def validate_swift_bank_account(self, swift):
        if swift:
            swift_bic_validator(swift)
        return swift

    def validate(self, data):
        if data['password1'] != data['password2']:
            raise serializers.ValidationError(
                _("The two password fields didn't match."))

        # Validation for professionals
        if data['type'] == PROFESSIONAL:
            #if not data.get('iban_bank_account') or not data.get('swift_bank_account'):
            #    raise serializers.ValidationError(_("Must include iban and swift account number 1."))
            if len(data.get('documents', [])) == 0:
                raise serializers.ValidationError(_("Must include one document at least"))
            if len(data.get('services', [])) == 0:
                raise serializers.ValidationError(_("Must include one services at least"))
            if len(data.get('work_zones', [])) == 0:
                raise serializers.ValidationError(_("Must include one work_zones at least"))
            if len(data.get('city', [])) == 0:
                raise serializers.ValidationError(_("Must include one city"))
        return data

    def get_cleaned_data(self):
        return {
            'first_name': self.validated_data.get('first_name', ''),
            'last_name': self.validated_data.get('last_name', ''),
            'password1': self.validated_data.get('password1', ''),
            'email': self.validated_data.get('email', '')
        }

    def get_profile_data(self):
        return {
            'type': self.initial_data.get('type', FINAL),
            'phone': self.initial_data.get('phone', ''),
            'picture': self.initial_data.get('picture', ''),
            'account_name': self.initial_data.get('account_name', ''),
            'iban_bank_account': self.initial_data.get('iban_bank_account', ''),
            'swift_bank_account': self.initial_data.get('swift_bank_account', ''),
            'documents': self.initial_data.get('documents', []),
            'work_days': self.initial_data.get('work_days', []),
            'work_hours': self.initial_data.get('work_hours', []),
            'city': self.initial_data.get('city', []),
            'fee': config.DEFAULT_PROFESSIONAL_FEE,
            'language': self.initial_data.get('language', 'en')
        }

    def save(self, request):
        adapter = get_adapter()
        user = adapter.new_user(request)
        self.cleaned_data = self.get_cleaned_data()
        adapter.save_user(request, user, self)
        setup_user_email(request, user, [])
        profile_data = self.get_profile_data()
        # Added custom information on registration (Profile, Services and Work_zones)
        ProfileOperator.create_profile(user, profile_data)  # Create Profile
        if self.initial_data.get('type') == PROFESSIONAL:
            ServicesOperator.create_services(user, self.initial_data.get('services'))  # Create UserServices
            WorZonesOperator.create_work_zones(user, self.initial_data.get('work_zones'))  # Create UserWorZones
        return user


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'
        read_only_fields = ('id', 'user',)

    def validate(self, data):
        # Validation for professionals
        if data.get('type') == PROFESSIONAL:
            #if not data.get('iban_bank_account') or not data.get('swift_bank_account'):
            #    raise serializers.ValidationError(_("Must include iban and swift account number 2."))
            if len(data.get('documents', [])) == 0:
                raise serializers.ValidationError(_("Must include one document at least"))
            if len(data.get('city', [])) == 0:
                raise serializers.ValidationError(_("Must include one city"))
        return data


class CustomResetPassword(PasswordResetSerializer):

    def save(self):
        request = self.context.get('request')
        # Set some values to trigger the send_email method.
        opts = {
            'use_https': request.is_secure(),
            'from_email': getattr(settings, 'DEFAULT_FROM_EMAIL'),
            'request': request,
            'html_email_template_name': 'registration/password_reset_email.html'
        }

        opts.update(self.get_email_options())
        self.reset_form.save(**opts)


class UserDetailsSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer()
    services = serializers.SerializerMethodField('get_user_services')
    work_zones = serializers.SerializerMethodField('get_user_work_zones')

    new_services = serializers.ListField(
        child=serializers.PrimaryKeyRelatedField(queryset=Service.objects.all().values_list('id', flat=True)),
        required=False, allow_null=True)
    new_zones = serializers.ListField(
        child=serializers.PrimaryKeyRelatedField(queryset=WorkZone.objects.all().values_list('id', flat=True)),
        required=False, allow_null=True)

    class Meta:
        model = UserModel
        fields = ('pk', 'username', 'email', 'first_name', 'last_name', 'profile', 'services', 'work_zones',
                  'new_zones', 'new_services')
        read_only_fields = ('email', 'username')

    def get_user_services(self, obj):
        return obj.get_user_services().values_list('id', flat=True)

    def get_user_work_zones(self, obj):
        return obj.get_user_work_zones().values_list('id', flat=True)

    def create_html_content(self, email, new_services):
        html_content = _("User") + ' ' + str(email) + ' ' + _("request to change his services")
        html_content += _("\n\nUser new services required are: ")
        for service in Service.objects.filter(pk__in=new_services):
            html_content += service.name
            html_content += ', '
        html_content += _("\n\nThese changes must be made manually by the administrator in web admin panel")
        return html_content

    def update(self, instance, validated_data):
        first_name = validated_data.get('first_name', instance.first_name)
        last_name = validated_data.get('last_name', instance.last_name)

        # Profile information
        profile = validated_data.get('profile', instance.profile)
        phone = profile.get('phone', instance.profile.phone)
        picture = profile.get('picture', instance.profile.picture)
        account_name = profile.get('account_name', instance.profile.account_name)
        language = profile.get('language', instance.profile.language)

        instance.first_name = first_name
        instance.last_name = last_name
        instance.profile.phone = phone
        instance.profile.picture = picture
        instance.profile.account_name = account_name
        instance.profile.language = language

        if instance.profile.type == PROFESSIONAL:
            swift_bank_account = profile.get('swift_bank_account', instance.profile.swift_bank_account)
            iban_bank_account = profile.get('iban_bank_account', instance.profile.iban_bank_account)
            documents = profile.get('documents', instance.profile.documents)
            work_days = profile.get('work_days', instance.profile.work_days)
            work_hours = profile.get('work_hours', instance.profile.work_hours)
            city = profile.get('city', instance.profile.city)

            instance.profile.swift_bank_account = swift_bank_account
            instance.profile.iban_bank_account = iban_bank_account
            instance.profile.documents = documents
            instance.profile.work_days = work_days
            instance.profile.work_hours = work_hours
            instance.profile.city = city

            new_zones = validated_data.get('new_zones')
            if new_zones:
                user_work_zones = WorZonesOperator.get_user_work_zones(instance).values_list('id', flat=True)
                diff_zones = list(set(user_work_zones) ^ set(new_zones))
                if len(diff_zones) != 0:
                    # To delete
                    zones_to_delete = list(set(user_work_zones) - set(new_zones))
                    UserWorkZone.objects.filter(user=instance, work_zone_id__in=zones_to_delete).delete()
                    # To create
                    zones_to_create = list(set(new_zones) - set(user_work_zones))
                    WorZonesOperator.create_work_zones(instance, zones_to_create)

            new_services = validated_data.get('new_services')
            if new_services:
                user_services = ServicesOperator.get_user_services(instance).values_list('id', flat=True)
                diff_services = list(set(user_services) ^ set(new_services))
                if len(diff_services) != 0:
                    subject = _("Request to change services user from user: ") + str(instance.email)
                    html_content = self.create_html_content(instance.email, new_services)
                    mail_managers(subject, html_content)
        instance.profile.save()
        instance.save()
        return instance


class UserListSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer()

    class Meta:
        model = UserModel
        fields = ('pk', 'username', 'email', 'first_name', 'last_name', 'profile')


