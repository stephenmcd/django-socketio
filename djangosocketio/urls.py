
from django.conf.urls.defaults import patterns, url


urlpatterns = patterns("djangosocketio.views",
    url("^socket\.io", "socketio", name="socketio"),
)
