from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from django.urls import re_path, path
from auction import consumers

websocket_urlpatterns = [
    path(r'ws/chat/', consumers.ChatConsumer.as_asgi()),
]