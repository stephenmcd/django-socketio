
from django.core.urlresolvers import reverse
from django.dispatch import receiver
from django.test import Client
from django.test import TestCase

from django_socketio import signals


class MockSocketIo(object):
    """
    Mock socket.io object for testing.
    """

    def __init__(self):
        self.recv_once = False

    def on_connect(self):
        return True

    def recv(self):
        """
        Return data once so that the ``on_message`` signal
        can be triggered.
        """
        if not self.recv_once:
            self.recv_once = True
            return ["test"]
        return []

    def connected(self):
        """
        Return True until data has been sent once.
        """
        return not self.recv_once

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

    def test_view(self):
        """
        Ensure the socketio view doesn't return errors.
        """
        response = SocketIoClient().get(reverse("socketio"))
        self.assertEqual(response.status_code, 200)

    def test_signals(self):
        """
        Ensure the socketio signals are received.
        """
        events = ["connect", "message", "disconnect", "finish"]

        on_connect = lambda **kwargs: events.remove("connect")
        receiver(signals.on_connect)(on_connect)

        on_message = lambda **kwargs: events.remove("message")
        receiver(signals.on_message)(on_message)

        on_disconnect = lambda **kwargs: events.remove("disconnect")
        receiver(signals.on_disconnect)(on_disconnect)

        on_finish = lambda **kwargs: events.remove("finish")
        receiver(signals.on_finish)(on_finish)

        response = SocketIoClient().get(reverse("socketio"))
        self.assertEqual(len(events), 0)

