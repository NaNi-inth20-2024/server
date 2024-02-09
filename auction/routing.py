from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from django.urls import re_path, path, include
from auction import consumers

websocket_urlpatterns = [
    re_path(r'ws/auctions/(?P<auction_id>\d+)/bids/$', consumers.AuctionConsumer.as_asgi()),
]

router = URLRouter(websocket_urlpatterns)
