# myproject/asgi.py

import os

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application

from realtime_app import routing # บรรทัดนี้ยังคงเดิม

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            routing.websocket_urlpatterns # <--- แก้ไขบรรทัดนี้ ให้ใช้ 'routing' โดยตรง
        )
    ),
})