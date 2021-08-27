from django.contrib.auth.models import User
from django.contrib.auth import get_user_model

from geo.models import WorkZone
from profiles.models import Profile, UserWorkZone
from services.models import UserService, Service, CityServices


class ProfileException(Exception):
    pass


class ProfileOperator(object):
    @staticmethod
    def create_profile(user, profile_data):
        if isinstance(user, User):
            profile = Profile.objects.create(
                user=user,
                **profile_data
            )
            return profile
        else:
            raise ProfileException('User is not an instance of User')


class ServicesOperator(object):
    @staticmethod
    def create_services(user, services):
        if isinstance(user, User):
            for service_id in services:
                service = Service.objects.get(pk=service_id)
                UserService.objects.create(
                    user=user,
                    service=service
                )
        else:
            raise ProfileException('User is not an instance of User')

    @staticmethod
    def get_user_services(user):
        if isinstance(user, User):
            services_id = UserService.objects.filter(user=user).values_list('service_id', flat=True)
            return Service.objects.filter(pk__in=services_id)
        else:
            return []

    @staticmethod
    def get_services_ids_by_zip_code(zip):
        cities = WorkZone.objects.filter(zip_codes__icontains=zip).values_list('city', flat=True)
        services_ids = CityServices.objects.filter(city_id__in=cities).values_list('service', flat=True)
        return list(services_ids)


class WorZonesOperator(object):
    @staticmethod
    def create_work_zones(user, work_zones):
        if isinstance(user, User):
            for work_zone_id in work_zones:
                work_zone = WorkZone.objects.get(pk=work_zone_id)
                UserWorkZone.objects.create(
                    user=user,
                    work_zone=work_zone
                )
        else:
            raise ProfileException('User is not an instance of User')

    @staticmethod
    def get_user_work_zones(user):
        if isinstance(user, User):
            work_zones_id = UserWorkZone.objects.filter(user=user).values_list('work_zone', flat=True)
            return WorkZone.objects.filter(pk__in=work_zones_id)
        else:
            return []

    @staticmethod
    def get_work_zones_by_zip(zip):
        return WorkZone.objects.filter(zip_codes__icontains=zip)

    @staticmethod
    def get_users_in_work_zone_by_zip(zip):
        work_zones = WorkZone.objects.filter(zip_codes__icontains=zip).values_list('id', flat=True)
        users_in_work_zones_ids = UserWorkZone.objects.filter(work_zone__in=work_zones).values_list('user', flat=True)
        return list(users_in_work_zones_ids)


def get_user_by_email(self):
    return '{}'.format(self.email)


UserModel = get_user_model()
UserModel.add_to_class('get_user_services', ServicesOperator.get_user_services)
UserModel.add_to_class('get_user_work_zones', WorZonesOperator.get_user_work_zones)
UserModel.add_to_class("__str__", get_user_by_email)
