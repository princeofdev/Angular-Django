# -*- coding: utf-8 -*-
from languages import languages
from django.conf import settings
from django.utils.translation import ugettext_lazy as _

ACTIVE = 'ACT'
INACTIVE = 'INA'

STATUS_TYPE = (
    (ACTIVE, _('Active')),
    (INACTIVE, _('Inactive')),
)

PRIVATE = 'PRI'
PUBLIC = 'PUB'

SERVICE_TYPE = (
    (PUBLIC, _('Public')),
    (PRIVATE, _('Private'))
)

PENDING = 'PEN'
ACCEPT = 'ACP'
COMPLETE = 'CMP'
CANCEL = 'CAN'
REJECT = 'REJ'
HIRE_SERVICE_TYPE = (
    (PENDING, _('Pending')),
    (ACCEPT, _('Accept')),
    (COMPLETE, _('Complete')),
    (CANCEL, _('Cancel')),
    (REJECT, _('Reject')),
)

languages.LANGUAGES = settings.LANGUAGES
