from django.db.models import Q
from django.utils.translation import ugettext as _

from profiles.models import UserWorkZone
from wuappa.filters import SingleTextInputFilter


class UserWorkZoneCountryFilter(SingleTextInputFilter):
    title = _('By user work zone Country')
    parameter_name = 'country'

    def queryset(self, request, queryset):
        if len(self.used_parameters) != 0 and self.value() != '':
            users_id = queryset.values_list('id', flat=True)
            users = UserWorkZone.objects.filter(
                Q(user_id__in=users_id),
                Q(work_zone__city__country__name=self.value()) |
                Q(work_zone__city__country__alternate_names__contains=self.value())
            ).values_list('user_id', flat=True)
            return queryset.filter(id__in=users)
        return queryset


class UserWorkZoneRegionFilter(SingleTextInputFilter):
    title = _('By user work zone Region')
    parameter_name = 'region'

    def queryset(self, request, queryset):
        if len(self.used_parameters) != 0 and self.value() != '':
            users_id = queryset.values_list('id', flat=True)
            users = UserWorkZone.objects.filter(
                Q(user_id__in=users_id),
                Q(work_zone__city__region__name=self.value()) |
                Q(work_zone__city__region__alternate_names__contains=self.value())
            ).values_list('user_id', flat=True)
            return queryset.filter(id__in=users)
        return queryset


class UserWorkZoneCityFilter(SingleTextInputFilter):
    title = _('By user work zone City')
    parameter_name = 'city'

    def queryset(self, request, queryset):
        if len(self.used_parameters) != 0 and self.value() != '':
            users_id = queryset.values_list('id', flat=True)
            users = UserWorkZone.objects.filter(
                Q(user_id__in=users_id),
                Q(work_zone__city__name=self.value()) |
                Q(work_zone__city__alternate_names__contains=self.value())
            ).values_list('user_id', flat=True)
            return queryset.filter(id__in=users)
        return queryset


class UserWorkZoneFilter(SingleTextInputFilter):
    title = _('By user work zone')
    parameter_name = 'workzone'

    def queryset(self, request, queryset):
        if len(self.used_parameters) != 0 and self.value() != '':
            users_id = queryset.values_list('id', flat=True)
            users = UserWorkZone.objects.filter(user_id__in=users_id,
                                                work_zone__name=self.value()
                                                ).values_list('user_id', flat=True)
            return queryset.filter(id__in=users)
        return queryset
