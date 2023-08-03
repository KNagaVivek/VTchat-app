
import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from channels.auth import AuthMiddlewareStack
from django.urls import path
from chat.consumers import *
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'VTchat.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter([
            path('ws/chat/<int:id>/', ChatConsumer.as_asgi()),
            path('ws/online/', OnlineStatusConsumer.as_asgi()),
        ]
        )
    )
})
