import csv
import re


from django.contrib import messages
from django.db.models import Q, Avg, Sum
from django.http import HttpResponseRedirect, HttpResponse
from django.middleware import csrf
from django.template import loader
from django.urls import reverse
from django.utils import translation
from django.utils.timezone import now, datetime
from django.utils.translation import ugettext as _
from django.views import View
from rest_framework import mixins, viewsets, status
from rest_framework.generics import ListCreateAPIView, CreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.response import Response

from coupon.models import UsedCoupon
from geo.models import WorkZone
from kf.viewsets import MultipleSerializersViewSet
from profiles.models import Profile
from profiles.serializers import UserListSerializer
from profiles.settings import FINAL, PROFESSIONAL
from services.filters import ServiceFilter, CategoryFilter
from services.models import Service, Category, HireService, UserService, HireServiceRefuse
from services.serializers import CategorySerializer, ServiceSerializer, HireServiceSerializer, \
    HireServiceCreateSerializer, HireServiceUpdateSerializer, ProfessionalAvailabilitySerializer, \
    ProfessionalCompleteSerializer, ProfessionalAcceptSerializer, ClientReviewSerializer, HireServiceDetailSerializer
from services.settings import ACTIVE, PUBLIC, PENDING, CANCEL, ACCEPT, COMPLETE, REJECT


class CategoryViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    List of categories.
    Can be filter by cities, zip, category, type and work_zones.
    """
    queryset = Category.objects.filter(status=ACTIVE).order_by('order')
    serializer_class = CategorySerializer
    permission_classes = ()
    pagination_class = None
    filter_class = CategoryFilter
    search_fields = ('name',)

    def get_queryset(self):
        if self.request.user.is_authenticated():
            return self.queryset
        else:
            return self.queryset.filter(type=PUBLIC)


class ServiceViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    List of services. Can be filter by type, category, cities and zip.
    """
    queryset = Service.objects.filter(
        status=ACTIVE, category__status=ACTIVE
    ).prefetch_related('city_services').order_by('order')
    serializer_class = ServiceSerializer
    permission_classes = ()
    pagination_class = None
    filter_class = ServiceFilter
    search_fields = ('name',)

    def get_serializer_context(self):
        context = super(ServiceViewSet, self).get_serializer_context()
        context["zip"] = self.request.query_params.get("zip")
        return context

    def get_queryset(self):
        if self.request.user.is_authenticated():
            return self.queryset
        else:
            return self.queryset.filter(type=PUBLIC, category__type=PUBLIC)


class HireServiceViewSet(MultipleSerializersViewSet, ListCreateAPIView, RetrieveUpdateDestroyAPIView):
    """
    list:
    List user hire services. If user is final show his hire services for the client.
    If user is professional show his services assigned for the professional.
    Can be filter by status
    If user is final an included ?review=true in url return the list of complete hire services for logged user without
    review.

    post:
    Contract services for a user in an address for a datetime.
    Total is required as Float and "total_currency" is optional

    update:
    Allow update a credit_card assigned to a hire service.

    update -> professional_accept_hire_service:
    Professional accept a hire service.

    update -> professional_complete_hire_service:
    Professional set a hire service as complete and charge total services.

    update -> client_review_hire_service:
    Client review a hire service complete.

    delete:
    A hire services is cancel.
    """
    queryset = HireService.objects.all().order_by('-date', '-time')
    serializer_class = HireServiceSerializer
    list_serializer_class = HireServiceSerializer
    retrieve_serializer_class = HireServiceDetailSerializer
    create_serializer_class = HireServiceCreateSerializer
    partial_update_serializer_class = HireServiceUpdateSerializer
    filter_fields = ('status',)

    @staticmethod
    def get_zip_codes(zip_codes_list):
        newlist = []
        for word in zip_codes_list:
            for el in word:
                el = el.split(" ")
                newlist.extend(el)
        return list(set(newlist))

    def perform_create(self, serializer):
        hire_service = serializer.save()
        if hire_service.coupon:
            UsedCoupon.objects.create(coupon=hire_service.coupon, user=self.request.user)

    def get_queryset(self):
        user = self.request.user

        if user.is_superuser:
            return HireService.objects.all().order_by('-date', '-time')

        if user.profile.type == FINAL:
            if self.request.query_params.get('review'):
                return HireService.objects.filter(client=user, status=COMPLETE, review_date__isnull=True).order_by('-date', '-time')
            else:
                return HireService.objects.filter(client=user).order_by('-date', '-time')
        elif user.profile.type == PROFESSIONAL:
            # Get zones by zip if not professional assigned
            zip_codes_list = list(WorkZone.objects.filter(work_zones__user=user).values_list('zip_codes', flat=True))
            zip_codes = self.get_zip_codes(zip_codes_list)
            user_services_ids = list(UserService.objects.filter(user=user).values_list('service_id', flat=True))
            refused_services = list(self.request.user.refused_services.all().values_list('service', flat=True))
            return HireService.objects.filter(Q(professional=user) | (
                Q(professional__isnull=True) & Q(status=PENDING) & (
                    Q(date__gt=now()) | (Q(date=now()) & Q(time__gt=now()))
                ) & Q(zip_code__in=zip_codes) & Q(services__in=user_services_ids)
            )).exclude(pk__in=refused_services).distinct().order_by('-date', '-time')
        else:
            return HireService.objects.none()

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # Bulk Update
    def bulk_update(self, request, *args, **kwargs):
        if len(request.data) == 2:
            if 'accept' in request.data and 'id' in request.data:
                return self.professional_accept_hire_service(self, request, *args, **kwargs)
            elif 'complete' in request.data and 'id' in request.data:
                return self.professional_complete_hire_service(self, request, *args, **kwargs)
        if len(request.data) == 3:
            if 'id' in request.data and 'review' in request.data and 'rating' in request.data:
                return self.client_review_hire_service(self, request, *args, **kwargs)

        return Response(status=status.HTTP_403_FORBIDDEN)

    def professional_accept_hire_service(self, req, *args, **kwargs):
        request = req.request
        serializer = ProfessionalAcceptSerializer(data=request.data, context=self.get_serializer_context())
        serializer.is_valid(raise_exception=True)

        hire_service_pk = serializer.data.get('id')
        result = HireService.objects.update_professional(hire_service_pk, serializer.validated_data.get('professional'))
        if result == 0:
            return Response({'error': _('Services has assigned to another professional')},
                            status=status.HTTP_400_BAD_REQUEST)

        return Response({}, status=status.HTTP_200_OK)

    def professional_complete_hire_service(self, req, *args, **kwargs):
        request = req.request
        serializer = ProfessionalCompleteSerializer(data=request.data, context=self.get_serializer_context())
        serializer.is_valid(raise_exception=True)

        try:
            hire_service = serializer.validated_data.get('id')
            amount = hire_service.total.amount
            # Create desciption
            services = hire_service.services.all()
            services_message = ''
            for service in services:
                services_message += str(service.name) + ', '

            description = _('Order id: %(id)s . Services: %(services)s') % {'id': hire_service.id,
                                                                            'services': services_message}
            hire_service.charge(amount=amount, description=description)
            # Update hire services status
            hire_service.status = COMPLETE
            hire_service.save()
            return Response(data=_("Charge add to client card."), status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'non_field_errors': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def client_review_hire_service(self, req, *args, **kwargs):
        request = req.request
        serializer = ClientReviewSerializer(data=request.data, context=self.get_serializer_context())
        serializer.is_valid(raise_exception=True)
        hire_service = serializer.validated_data.get('id')
        hire_service.rating = serializer.validated_data.get('rating')
        hire_service.review = serializer.validated_data.get('review')
        hire_service.review_date = now()
        hire_service.notified_at = now()
        hire_service.save()
        professional_average = HireService.objects.filter(professional=hire_service.professional,
                                                          status=COMPLETE, rating__isnull=False,
                                                          rating__gt=0).aggregate(average=Avg('rating'))
        if professional_average.get('average') is not None:
            Profile.objects.filter(pk=hire_service.professional.profile.pk).update(rating=professional_average.get('average'))
        return Response(data=_("Added Review to hire services."), status=status.HTTP_200_OK)

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.client != self.request.user and \
                (instance.professional != self.request.user and instance.status != PENDING):
            return Response(status=status.HTTP_403_FORBIDDEN)

        if self.request.user.profile.type == PROFESSIONAL:
            if instance.status == PENDING:
                new_status = PENDING
            else:
                new_status = REJECT
        else:
            new_status = CANCEL

        services_datetime = datetime.combine(instance.date, instance.time).replace(tzinfo=None)

        if instance.status == ACCEPT and new_status == REJECT:
            if services_datetime < now().replace(tzinfo=None):
                return Response({'error': _('Services can\'t be cancel. Service date has passed.')},
                                status=status.HTTP_400_BAD_REQUEST)
            else:
                instance.status = new_status

        elif instance.status == ACCEPT and new_status == CANCEL:
            cancel_amount = instance.calc_cancelability_cost()
            if cancel_amount > 0:
                try:
                    services = instance.services.all()
                    services_message = ''
                    for service in services:
                        services_message += str(service.name) + ', '

                    description = _('Service cancel. Order id: %(id)s. Services: %(services)s') % {'id': instance.id,
                                                                                                   'services': services_message}
                    instance.charge(amount=cancel_amount, description=description)
                except Exception as e:
                    return Response({'non_field_errors': str(e)}, status=status.HTTP_400_BAD_REQUEST)

            instance.status = new_status

        elif instance.status in [COMPLETE, REJECT, CANCEL]:
            return Response({'error': _('Services can\'t be cancel. Service status is %(status)s.')
                            % {'status': instance.status}}, status=status.HTTP_400_BAD_REQUEST)

        else:   # status == PENDING
            if self.request.user.profile.type == PROFESSIONAL:
                HireServiceRefuse.objects.create(user=self.request.user, service=instance)
            instance.status = new_status
        instance.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def cancelability(self, request, pk):
        """
        Returns if a HireService is cancelable
        :param request: request
        :param pk: HireService pk
        :return:
        """
        try:
            service = self.get_queryset().get(pk=pk)
            amount = service.calc_cancelability_cost()
            response_status = status.HTTP_200_OK if amount == 0 else status.HTTP_400_BAD_REQUEST
            return Response({'amount': amount, 'currency': service.total_currency}, status=response_status)
        except HireService.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def notify_customer(self, request, pk):
        """
        Notify user that it's wuapper is on its way
        :param request: request
        :param pk: HireService pk
        :return:
        """
        try:
            service = self.get_queryset().get(pk=pk)
            translation.activate(service.client.profile.language)
            name = '{0} {1}'.format(service.professional.first_name, service.professional.last_name)
            message = _('Your WUAPPER {0} is on its way').format(name)
            service.send_push_notification_to_client(message)
            return Response({'status': 'sent'}, status=status.HTTP_200_OK)
        except HireService.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


class ProfessionalAvailabilityViewSet(MultipleSerializersViewSet, CreateAPIView):
    """
    post:
    Return professionals that can make a work for a client request.
    """
    create_serializer_class = ProfessionalAvailabilitySerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        services = request.data.get('services')
        zip = request.data.get('zip')
        date = datetime.strptime("{0} {1}".format(
            request.data.get('date'), request.data.get('time')
        ), "%Y-%m-%d %H:%M")
        time = request.data.get('time')

        if date.replace(tzinfo=None) < now().replace(tzinfo=None):
            return Response(
                {'error': _('The selected date and time is in the past.')},
                status=status.HTTP_400_BAD_REQUEST
            )

        professionals = HireService.objects.available_professionals_for_service(services, zip, date, date.hour)
        if professionals is None:
            return Response(
                {'error': _('Services included are not included for that work zone')},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = UserListSerializer(professionals, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ServicesExportReport(View):

    def get(self, request):
        user = self.request.user if self.request.user else None
        if not user.is_authenticated():
            return HttpResponseRedirect(reverse('admin:index'))
        start_date = finish_date = ''
        t = loader.get_template('admin/services_export.html')
        c = {'start_date': start_date, 'finish_date': finish_date, 'csrftoken': csrf.get_token(request)}
        return HttpResponse(t.render(c, request=request))

    def post(self, request):
        date_r = r'[0-9]{4}-[0-9]{2}-[0-9]{2}'
        start_date = request.POST.get('start_date', '')
        finish_date = request.POST.get('finish_date', '')
        error = False

        if re.match(date_r, start_date) is None or re.match(date_r, finish_date) is None:
            if re.match(date_r, start_date) is None:
                messages.error(request, 'Star date is required')
            if re.match(date_r, finish_date) is None:
                messages.error(request, 'Finish date is required')
            error = True

        try:
            start_date = datetime.datetime.strptime(start_date, '%Y-%m-%d')
        except ValueError as e:
            error = True
            messages.error(request, 'Star date format error: %s' % e)
        try:
            finish_date = datetime.datetime.strptime(finish_date, '%Y-%m-%d')
        except ValueError as e:
            error = True
            messages.error(request, 'Finish date format error: %s' % e)

        if error:
            t = loader.get_template('admin/services_export.html')
            c = {'start_date': start_date, 'finish_date': finish_date, 'csrftoken': csrf.get_token(request)}
            return HttpResponse(t.render(c, request=request))

        hire_services = HireService.objects.filter(
            professional__isnull=False, status='CMP', date__gte=start_date, date__lte=finish_date
        ).values(
            'professional__first_name',
            'professional__last_name',
            'professional__profile__account_name',
            'professional__profile__iban_bank_account',
            'professional__profile__swift_bank_account',
            'professional__profile__fee',
            'total_currency').annotate(
            total=Sum('total_charged'),
            net_total=Sum('net_total')
        ).order_by('professional__id')

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="services.csv"'

        writer = csv.writer(response)

        csv_header = ['First Name', 'Last name', 'Account name', 'SWIFT', 'IBAN', 'Total', 'Net total', 'FEE',
                      'Net total without fee']
        writer.writerow(csv_header)

        for item in hire_services:
            csv_line = list()
            csv_line.append(item.get('professional__first_name'))
            csv_line.append(item.get('professional__last_name'))
            csv_line.append(item.get('professional__profile__account_name'))
            csv_line.append(item.get('professional__profile__iban_bank_account'))
            csv_line.append(item.get('professional__profile__swift_bank_account'))
            csv_line.append(item.get('total'))
            csv_line.append(item.get('net_total'))
            csv_line.append(float(item.get('professional__profile__fee', '0') or '0') * float(item.get('net_total', '0') or '0') / 100.0)
            csv_line.append(float(item.get('net_total', '0') or '0') - (item.get('professional__profile__fee', 0) or 0) * float(item.get('net_total', '0') or '0') / 100.0)
            writer.writerow(csv_line)

        return response
