
from django.conf import settings
from django.conf.urls.defaults import patterns, include, url
from django.views.generic.simple import direct_to_template


urlpatterns = patterns('',
    url("", include("django_socketio.urls")),
    url("^$", direct_to_template, {"template": "index.html"}, name="index"),
    ("^%s/(?P<path>.*)$" % settings.MEDIA_URL.strip("/"),
        "django.views.static.serve", {"document_root":  settings.MEDIA_ROOT}),
)
