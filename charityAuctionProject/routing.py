from channels.routing import URLRouter
from django.urls import re_path

from auction.routing import router

websocket_urlpatterns = [
    re_path(r'api/v1/ws', router),
]

router = URLRouter(
    websocket_urlpatterns
)