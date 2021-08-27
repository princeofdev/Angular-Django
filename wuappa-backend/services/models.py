import datetime

from dateutil import relativedelta
from decimal import Decimal
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.utils.translation import ugettext as _
from djmoney.models.fields import MoneyField
from djstripe.models import Charge, Customer
from push_notifications.models import GCMDevice, APNSDevice

from geo.models import City, Country, Region, WorkZone
from services.managers import HireServiceManager
from services.settings import STATUS_TYPE, ACTIVE, SERVICE_TYPE, PUBLIC, HIRE_SERVICE_TYPE, PENDING
from services.validators import check_credit_card
from coupon.models import Coupon


class Category(models.Model):

    name = models.CharField(max_length=150)
    image = models.FileField(null=True, blank=True)
    type = models.CharField(max_length=3, choices=SERVICE_TYPE, default=PUBLIC)
    status = models.CharField(max_length=3, choices=STATUS_TYPE, default=ACTIVE)
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ('order',)

    def __str__(self):
        return self.name

    def get_cities(self):
        services = Service.objects.filter(category=self)
        return CityServices.objects.filter(service__in=services)


class Service(models.Model):
    category = models.ForeignKey(Category)
    name = models.CharField(max_length=150)
    description = models.TextField(null=True, blank=True)
    image = models.FileField(null=True, blank=True)
    status = models.CharField(max_length=3, choices=STATUS_TYPE, default=ACTIVE)
    type = models.CharField(max_length=3, choices=SERVICE_TYPE, default=PUBLIC)
    order = models.IntegerField(default=0)
    preparation = models.TextField(null=True, blank=True)
    time = models.CharField(max_length=100, null=True, blank=True)

    class Meta:
        ordering = ('order',)

    def __str__(self):
        return "%s - %s" % (self.name, self.category.name)

    def get_cities(self):
        return CityServices.objects.filter(service=self)


class CityServices(models.Model):
    city = models.ForeignKey(City, related_name='cities', verbose_name=_("City"))
    service = models.ForeignKey(Service, related_name='city_services', verbose_name=_("Service"))
    price = MoneyField(max_digits=10, decimal_places=2, default_currency='CHF')
    vat_percent = models.FloatField(default=7.7)

    class Meta:
        ordering = ('service__order',)

    def __str__(self):
        return "%s - Service: %s. Price: %s" % (self.city.name, self.service.name, self.price)


class UserService(models.Model):
    user = models.ForeignKey(User, related_name='user_services', verbose_name=_("User"))
    service = models.ForeignKey(Service, related_name='services', verbose_name=_("Service"))

    def __str__(self):
        return "%s - %s" % (self.user.email, self.service.name)


class HireService(models.Model):
    client = models.ForeignKey(User, related_name='client', verbose_name=_("Client"))
    professional = models.ForeignKey(User, null=True, blank=True, related_name='professional',
                                     verbose_name=_("Professional"))
    date = models.DateField()
    time = models.TimeField()
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    region = models.CharField(max_length=255)
    zip_code = models.CharField(max_length=10)
    country = models.CharField(max_length=255)
    services = models.ManyToManyField('Service', through='HireServiceService', related_name='hirings')
    comments = models.TextField(null=True, blank=True)
    status = models.CharField(max_length=3, choices=HIRE_SERVICE_TYPE, default=PENDING)

    credit_card = models.CharField(max_length=255, validators=[check_credit_card])
    total = MoneyField(max_digits=10, decimal_places=2, default_currency='CHF')
    vat = MoneyField(default=0, max_digits=10, decimal_places=2, default_currency='CHF')
    net_total = MoneyField(default=0, max_digits=10, decimal_places=2, default_currency='CHF')

    total_charged = MoneyField(default=0, max_digits=10, decimal_places=2, default_currency='CHF')
    vat_charged = MoneyField(default=0, max_digits=10, decimal_places=2, default_currency='CHF')
    net_charged = MoneyField(default=0, max_digits=10, decimal_places=2, default_currency='CHF')

    charges = models.ForeignKey(Charge, null=True, blank=True)

    modified_at = models.DateTimeField(auto_now=True)
    notified_at = models.DateTimeField(null=True, blank=True, default=None)

    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)], null=True, blank=True)
    review = models.TextField(null=True, blank=True)
    review_date = models.DateField(null=True, blank=True, default=None)

    objects = HireServiceManager()

    coupon = models.ForeignKey(Coupon, null=True, blank=True, default=None)

    def calc_cancelability_cost(self):
        service_datetime = datetime.datetime.combine(self.date, self.time)
        difference = relativedelta.relativedelta(service_datetime, datetime.datetime.now())
        if difference.days == 0:
            if difference.hours >= 12:  # Charge 50% of service total
                return round(Decimal(self.total.amount / 2), 2)
            else:  # difference.hours <= 12 -> Charge 100% of hire service total
                return self.total.amount
        return 0

    def charge(self, amount, description):
        customer, created = Customer.get_or_create(self.client)
        charge = customer.charge(
            amount=amount, currency=self.total_currency, description=description, source=self.credit_card
        )
        self.charges = charge

        # Calculating total charged
        percent_charged = float(amount) / float(self.total)
        self.total_charged = amount
        self.vat_charged = self.vat * percent_charged
        self.net_charged = self.net_total * percent_charged

        self.save()

    def send_push_notification_to_client(self, message):
        extra = dict()
        message_data = {"title": "Wuappa", "body": str(message)}
        if self.client:
            APNSDevice.objects.filter(user=self.client).send_message(
                message=message_data,
                extra=extra,
                sound="default"
            )
            GCMDevice.objects.filter(user=self.client).send_message(
                message=message_data.get("body"),
                title=message_data.get("title"),
                extra=extra,
                icon="notification",
                sound=True
            )

    def __str__(self):
        return "User: %s. %s - %s" % (self.client.email, self.date, self.time)


class HireServiceRefuse(models.Model):

    user = models.ForeignKey(User, related_name='refused_services')
    service = models.ForeignKey(HireService)


class HireServiceService(models.Model):

    hireservice = models.ForeignKey(HireService)
    service = models.ForeignKey(Service)
