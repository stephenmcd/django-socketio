
from django.core.handlers.base import BaseHandler
from django.core.handlers.wsgi import WSGIRequest
from django.core.urlresolvers import reverse
from django.test import Client
from django.test import TestCase


class MockSocketIo(object):
    """
    Mock socket.io object for testing.
    """
    def on_connect(self):
        return True
    def recv(self):
        return ""
    def connected(self):
        return False

class SocketIoClient(Client):
    """
    Test client that adds a mocked socketio object to the
    environment dictionary.
    """
    def _base_environ(self, **request):
        environ = super(Client, self)._base_environ(**request)
        environ["socketio"] = MockSocketIo()
        return environ

class Tests(TestCase):
    """
    django-socketio tests.
    """

    def test_socketio(self):
        """
        Ensure the socketio view doesn't return errors.
        """
        response = SocketIoClient().get(reverse("socketio"))
        self.assertEqual(response.status_code, 200)
