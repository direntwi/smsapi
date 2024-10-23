from django.urls import path, re_path
from . import consumers

websocket_urlpatterns = [
    path("ws/dlr-updates/", consumers.DLRConsumer.as_asgi()),
]
