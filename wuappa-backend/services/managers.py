import datetime

from django.contrib.auth.models import User
from django.db import models
from django.utils.timezone import now

from services.settings import PENDING, ACCEPT
from work_calendars.models import DayOff


class HireServiceManager(models.Manager):

    @staticmethod
    def get_weekday_for_date(date):
        days = [1, 2, 3, 4, 5, 6, 0]
        day_number = date.weekday()
        return days[day_number]

    def update_professional(self, pk, professional):
        return self.get_queryset().filter(pk=pk, professional__isnull=True, status=PENDING).update(
            professional=professional, status=ACCEPT, modified_at=now())

    def available_professionals_for_service(self, services, zip, date, time):
        from profiles.utils import ServicesOperator, WorZonesOperator
        from services.models import UserService, HireService

        services_ids = ServicesOperator.get_services_ids_by_zip_code(zip)

        # Check if all client selected service are available for the zip
        if not all(x in services_ids for x in services):
            return None

        # Second, get users works in that work_zone and works in that time
        users_in_work_zones_ids = WorZonesOperator.get_users_in_work_zone_by_zip(zip)
        users_in_work_zones_with_services_ids = list(UserService.objects.filter(
            user_id__in=users_in_work_zones_ids, service_id__in=services
        ).values_list('user_id', flat=True))
        weekday = self.get_weekday_for_date(date)
        professionals = User.objects.filter(id__in=users_in_work_zones_with_services_ids,
                                            profile__work_days__contains=[weekday],
                                            profile__work_hours__contains=[time])

        # Then, exclude professional with hire service for that date and time
        time_format = str(time) + ':00:00' if time >= 10 else '0' + str(time) + ':00:00'
        professionals_with_hire_services = list(
            HireService.objects.filter(
                professional__in=list(professionals), status=ACCEPT, date=date, time=time_format
            ).values_list('professional', flat=True)
        )
        professionals = professionals.exclude(id__in=professionals_with_hire_services)

        # Finally, exclude professionals id date include in his day off
        professionals_with_day_off = list(DayOff.objects.filter(
            professional__in=list(professionals), date=date).values_list('professional', flat=True)
        )
        return professionals.exclude(id__in=professionals_with_day_off)
