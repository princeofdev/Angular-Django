# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand
from django.db.models import Q, F
from django.utils import translation
from django.utils.timezone import now
from push_notifications import NotificationError
from push_notifications.models import GCMDevice, APNSDevice
from django.utils.translation import ugettext_lazy as _
from django.conf import settings

from services.models import HireService
from services.settings import PENDING, ACCEPT, CANCEL, REJECT, COMPLETE


class Command(BaseCommand):
    help = 'Send pending push notificacions'

    def send_push_notificacions_to_users(self, users, message, params=list(), extra=dict()):
        self.stdout.write("Sending messages to: {0}".format(' '.join([user.email for user in users])))
        for language in settings.LANGUAGES:
            language_code = language[0]
            self.stdout.write("Sending messages in {0}".format(language_code))
            translation.activate(language_code)
            message_data = {
                "title": "Wuappa",
                "body": str(_(message)).format(*params)
            }

            # APNS devices
            try:
                APNSDevice.objects.filter(user__in=users, user__profile__language=language_code).send_message(
                    message=message_data,
                    extra=extra,
                    sound="default"
                )
            except NotificationError as e:
                self.stderr.write("Error while sending APNS notifications")
                self.stderr.write(e)

            # GCM devices
            try:
                GCMDevice.objects.filter(user__in=users, user__profile__language=language_code).send_message(
                    message=message_data.get("body"),
                    title=message_data.get("title"),
                    extra=extra,
                    icon="notification",
                    sound=True
                )
            except NotificationError as e:
                self.stderr.write("Error while sending GCM notifications")
                self.stderr.write(e)

    def handle(self, *args, **options):

        # Notifying pending services to professionals
        pending_services_to_notify_qs = HireService.objects.filter(
            Q(notified_at__isnull=True) | Q(modified_at__gt=F('notified_at')),
            Q(date__gt=now()) | (Q(date=now()) & Q(time__gt=now())),
            status=PENDING
        )
        pending_services_to_notify = list(pending_services_to_notify_qs)
        self.stdout.write("Sending {0} pending services notifications...".format(len(pending_services_to_notify)))
        pending_services_to_notify_qs.update(notified_at=now())
        professionals_with_pending_services = list()
        for service in pending_services_to_notify:
            time = int(str(service.time).split(":")[0]) if ":" in str(service.time) else 0
            services_ids = [service.pk for service in service.services.all()]
            professionals = HireService.objects.available_professionals_for_service(
                services_ids, service.zip_code, service.date, time
            )
            professionals_with_pending_services.extend(list(professionals))

        extra = {"type": "service.pending"}
        self.send_push_notificacions_to_users(
            list(professionals_with_pending_services), "You have pending services available", extra=extra
        )

        # Notifying accepted services to customers
        accepted_services_to_notify_qs = HireService.objects.filter(
            Q(notified_at__isnull=True) | Q(modified_at__gt=F('notified_at')), status=ACCEPT
        )
        accepted_services_to_notify = list(accepted_services_to_notify_qs)
        self.stdout.write("Sending {0} accepted services notifications...".format(len(accepted_services_to_notify)))
        accepted_services_to_notify_qs.update(notified_at=now())
        for service in accepted_services_to_notify:
            extra = {"id": service.pk, "type": "service.update"}
            self.send_push_notificacions_to_users([service.client], "Service on {0} at {1} accepted by {2} {3}", params=[
                service.date.strftime("%d/%m"), service.time.strftime("%H:%M"),
                service.professional.first_name, service.professional.last_name
            ], extra=extra)

        # Notifying canceled services to professionals
        canceled_services_to_notify_qs = HireService.objects.filter(
            Q(notified_at__isnull=True) | Q(modified_at__gt=F('notified_at')), status=CANCEL
        )
        canceled_services_to_notify = list(canceled_services_to_notify_qs)
        self.stdout.write("Sending {0} canceled services notifications...".format(len(canceled_services_to_notify)))
        canceled_services_to_notify_qs.update(notified_at=now())
        for service in canceled_services_to_notify:
            extra = {"id": service.pk, "type": "service.update"}
            self.send_push_notificacions_to_users([service.professional], "Service on {0} at {1} canceled by {2} {3}", params=[
                service.date.strftime("%d/%m"), service.time.strftime("%H:%M"),
                service.client.first_name, service.client.last_name
            ], extra=extra)

        # Notifying rejected services to customers
        rejected_services_to_notify_qs = HireService.objects.filter(
            Q(notified_at__isnull=True) | Q(modified_at__gt=F('notified_at')), status=REJECT
        )
        rejected_services_to_notify = list(rejected_services_to_notify_qs)
        self.stdout.write("Sending {0} rejected services notifications...".format(len(rejected_services_to_notify)))
        rejected_services_to_notify_qs.update(notified_at=now())
        for service in rejected_services_to_notify:
            extra = {"id": service.pk, "type": "service.update"}
            self.send_push_notificacions_to_users([service.client], "Service on {0} at {1} canceled by {2} {3}", params=[
                service.date.strftime("%d/%m"), service.time.strftime("%H:%M"),
                service.professional.first_name, service.professional.last_name
            ], extra=extra)

        # Notifying completed services to customers
        completed_services_to_notify_qs = HireService.objects.filter(review_date__isnull=True).filter(
            Q(notified_at__isnull=True) | Q(modified_at__gt=F('notified_at')), status=COMPLETE
        )
        completed_services_to_notify = list(completed_services_to_notify_qs)
        self.stdout.write("Sending {0} completed services notifications...".format(len(completed_services_to_notify)))
        completed_services_to_notify_qs.update(notified_at=now())
        for service in completed_services_to_notify:
            extra = {"id": service.pk, "type": "service.update"}
            self.send_push_notificacions_to_users([service.client], "Service on {0} at {1} completed by {2} {3}", params=[
                service.date.strftime("%d/%m"), service.time.strftime("%H:%M"),
                service.professional.first_name, service.professional.last_name
            ], extra=extra)
