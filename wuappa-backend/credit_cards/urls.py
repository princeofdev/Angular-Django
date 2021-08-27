from rest_framework import routers

from credit_cards.views import CardViewSet

router = routers.SimpleRouter()

router.register(r'1.0/cards', CardViewSet, base_name="cards")

urlpatterns = router.urls
