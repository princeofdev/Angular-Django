from rest_framework import routers

from geo.views import CountryViewSet, RegionViewSet, CityViewSet, WorkZoneViewSet

router = routers.SimpleRouter()

router.register(r'1.0/countries', CountryViewSet)
router.register(r'1.0/regions', RegionViewSet)
router.register(r'1.0/cities', CityViewSet)
router.register(r'1.0/zones', WorkZoneViewSet)

urlpatterns = router.urls