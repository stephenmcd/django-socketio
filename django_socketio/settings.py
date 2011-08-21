
from django.conf import settings

HOST = getattr(settings, "SOCKETIO_HOST", "127.0.0.1")
PORT = getattr(settings, "SOCKETIO_PORT", 9000)

