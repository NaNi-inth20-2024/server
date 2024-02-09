from channels.routing import URLRouter
from django.urls import re_path

from auction import consumers

websocket_urlpatterns = [
    re_path(r'auctions/(?P<auction_id>\d+)/bids/$', consumers.AuctionConsumer.as_asgi()),
]

router = URLRouter(websocket_urlpatterns)
