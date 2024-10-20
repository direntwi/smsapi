from django.urls import path
from . import consumers

websocket_urlpatterns = [
    path("ws/dlr-updates/", consumers.DLRConsumer.as_asgi()),
]
