
from django.conf.urls.defaults import patterns, url


urlpatterns = patterns("django_socketio.views",
    url("^socket\.io", "socketio", name="socketio"),
)
