
from django.conf.urls import url

from gift_card.api import GiftCardListAPI

urlpatterns = [
    url(r'1.0/gift_card/(?P<code>[0-9a-zA-Z]+)', GiftCardListAPI.as_view(), name="gift_card_api"),
    url(r'1.0/gift_card/create', GiftCardListAPI.as_view(), name="gift_card_create_api")
]