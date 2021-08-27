from rest_framework.routers import SimpleRouter

from work_calendars.views import DayOffViewSet

day_off_router = SimpleRouter()
day_off_router.register(r'1.0/days-off', DayOffViewSet)
urlpatterns = day_off_router.urls
