
from django.dispatch import Signal


on_connect      = Signal(providing_args=["socket"])
on_message      = Signal(providing_args=["socket", "message"])
on_subscribe    = Signal(providing_args=["socket", "channel"])
on_unsubscribe  = Signal(providing_args=["socket", "channel"])
on_error        = Signal(providing_args=["socket", "exception"])
on_disconnect   = Signal(providing_args=["socket"])
on_finish       = Signal(providing_args=["socket"])
