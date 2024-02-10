from channels.routing import URLRouter
from django.urls import re_path

from auction.routing import router
from charityAuctionProject.wss import MyConsumer

websocket_urlpatterns = [
    re_path(r'^api/v1/ws', router),
    re_path(r'ws', MyConsumer.as_asgi()),
]

router = URLRouter(websocket_urlpatterns)
