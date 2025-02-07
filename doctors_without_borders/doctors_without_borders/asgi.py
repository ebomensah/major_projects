import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "doctors_without_borders.settings")

django_asgi_app = get_asgi_application()

import chat.routing  # Import the routing.py file from your chat app

application = ProtocolTypeRouter({
    "http": django_asgi_app,  # Standard Django HTTP handling
    "websocket": AuthMiddlewareStack(  # WebSocket handling
        URLRouter(
            chat.routing.websocket_urlpatterns
        )
    ),
})