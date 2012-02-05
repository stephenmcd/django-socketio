
from django.conf import settings

HOST = getattr(settings, "SOCKETIO_HOST", "127.0.0.1")
PORT = getattr(settings, "SOCKETIO_PORT", 9000)
MESSAGE_LOG_FORMAT = getattr(settings, "SOCKETIO_MESSAGE_LOG_FORMAT",
                             '%(REMOTE_ADDR)s - - [%(TIME)s] '
                             '"Socket.IO %(TYPE)s: %(MESSAGE)s"')
