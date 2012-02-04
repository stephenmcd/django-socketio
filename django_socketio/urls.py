
from django.conf.urls.defaults import patterns, url
from django.conf import settings
from django.utils.importlib import import_module


# Try and import an ``events`` module in each installed app,
# to ensure all event handlers are connected.
for app in settings.INSTALLED_APPS:
    try:
        import_module("%s.events" % app)
    except ImportError:
        pass


urlpatterns = patterns("django_socketio.views",
    url("^socket\.io", "socketio", name="socketio"),
)
