
from django.template import Library


register = Library()

@register.inclusion_tag("socketio_scripts.html", takes_context=True)
def socketio(context):
    return context
