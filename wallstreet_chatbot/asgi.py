import os

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter ,ChannelNameRouter
import chat.routing
from chat import consumers
from channels.layers import get_channel_layer

channel_layer = get_channel_layer()


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "wallstreet_chatbot.settings")

application = ProtocolTypeRouter({
  "websocket": AuthMiddlewareStack(
        URLRouter(
            chat.routing.websocket_urlpatterns
        )
    ),
})

