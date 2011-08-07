
from django.core.urlresolvers import reverse
from django.test import Client
from django.test import TestCase

from django_socketio import events


class MockAttributes(object):
    """
    A callable object that will always return a value for missing
    attributes accessed. The value returned is a new MockAttributes
    instance allowing for successful chained attribute access.
    """

    def __getattr__(self, name):
        """
        Store the value returned so that the same object is always
        given when the attribute is accessed. Required for correct
        results when used as a dictionary key.
        """
        setattr(self, name, MockAttributes())
        return getattr(self, name)

    def __call__(self, *args, **kwargs):
        return None

class MockSocketIo(MockAttributes):
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
        can be triggered when testing.
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

    def test_signals_and_response(self):
        """
        Ensure that the socketio view returns a valid response and
        that signals are received. Signals are checked by pulling
        each event name off a list of events. The error event should
        be the only remaning. The connect signal is used to remove
        any non-test message handlers since there's no guarantee the
        mock socketio object will return the data they expect.
        """

        event_names = ["connect", "message", "disconnect", "finish", "error"]
        test_uid = "message_test"

        @events.on_connect
        def on_connect(*args):
#            r = [r for r in signals.on_message.receivers if r[0][0] == test_uid]
#            signals.on_message.receivers = r
            event_names.remove("connect")

        @events.on_message
        def on_message(*args):
            event_names.remove("message")

        @events.on_disconnect
        def on_disconnect(*args):
            event_names.remove("disconnect")

        @events.on_finish
        def on_finish(*args):
            event_names.remove("finish")

        @events.on_error
        def on_error(*args):
            event_names.remove("error")

        response = SocketIoClient().get(reverse("socketio"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(event_names), 1)
        self.assertEqual(event_names[0], "error")
