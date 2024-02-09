from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import include, path, re_path

from auction import consumers

websocket_urlpatterns = [
    re_path(r"ws/auctions/(?P<auction_id>\d+)/bids/$", consumers.AuctionConsumer.as_asgi()),
]

router = URLRouter(websocket_urlpatterns)
