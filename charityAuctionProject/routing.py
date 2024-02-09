from channels.routing import URLRouter
from django.urls import path, re_path
from auction.routing import router

websocket_urlpatterns = [
    path(r'api/v1/ws', router),
]

router = URLRouter(
    websocket_urlpatterns
)