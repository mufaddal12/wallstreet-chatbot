from django.urls import re_path
from django.conf.urls import url
from channels.routing import ChannelNameRouter
from django.urls import path
from . import consumers

websocket_urlpatterns = [
    path('ws/app/<str:room_name>/', consumers.ChatConsumer.as_asgi()),
]   

# ChannelNameRouter({
#     "roomchat": consumers.ChatConsumer.as_asgi(),
# })