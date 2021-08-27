from rest_framework import routers
from rest_framework.routers import Route

from services.views import ServiceViewSet, CategoryViewSet, HireServiceViewSet, ProfessionalAvailabilityViewSet

router = routers.SimpleRouter()


class HireServiceRouter(routers.SimpleRouter):
    routes = [
        Route(
            url=r'^{prefix}/$',
            mapping={'get': 'list', 'post': 'create', 'put': 'bulk_update'},
            name='{basename}-list',
            initkwargs={'suffix': 'List'}
        ),
        Route(
            url=r'^{prefix}/{lookup}/$',
            mapping={'put': 'update', 'patch': 'partial_update', 'delete': 'delete', 'get': 'retrieve'},
            name='{basename}-detail',
            initkwargs={'suffix': 'Detail'}
        ),
        Route(
            url=r'^{prefix}/{lookup}/cancelability/$',
            mapping={'get': 'cancelability'},
            name='{basename}-service-cancelability',
            initkwargs={'suffix': 'Cancelability'}
        ),
        Route(
            url=r'^{prefix}/{lookup}/notify-customer/$',
            mapping={'post': 'notify_customer'},
            name='{basename}-service-notify-customer',
            initkwargs={'suffix': 'NotifyCustomer'}
        )
    ]


hire_service_router = HireServiceRouter()
hire_service_router.register(r'1.0/hire-services', HireServiceViewSet)


router.register(r'1.0/categories', CategoryViewSet)
router.register(r'1.0/services', ServiceViewSet)
router.register(r'1.0/professionals-availability', ProfessionalAvailabilityViewSet,
                base_name='professionals-availability')

urlpatterns = router.urls + hire_service_router.urls
