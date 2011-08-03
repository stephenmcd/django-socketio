
from django.dispatch import receiver
from django_socketio import signals
from django.utils.html import strip_tags


@receiver(signals.on_connect)
def connect(request=None, socket=None, **kwargs):
    pass

@receiver(signals.on_message)
def message(request=None, socket=None, message=None, **kwargs):
    for field in ("name", "message"):
        message[0][field] = strip_tags(message[0][field])
    socket.send(message[0])
    socket.broadcast(message[0])
