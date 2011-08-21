
from os import environ

from django.template import Library


register = Library()

@register.inclusion_tag("socketio_scripts.html", takes_context=True)
def socketio(context):
    context["DJANGO_SOCKETIO_PORT"] = environ["DJANGO_SOCKETIO_PORT"]
    return context
