
from django_socketio import signals


def connect(request, socket, **kwargs):
    pass

signals.on_connect.connect(connect)
