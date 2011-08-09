
from django.conf import settings
from django.conf.urls.defaults import patterns, include, url


urlpatterns = patterns('',
    url("", include("django_socketio.urls")),
    url("", include("chat.urls")),
)
