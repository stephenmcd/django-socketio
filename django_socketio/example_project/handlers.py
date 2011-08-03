
from django.dispatch import receiver
from django_socketio import signals


@receiver(signals.on_connect)
def connect(request=None, socket=None, **kwargs):
    pass

