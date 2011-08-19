
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
        each event name off a list of events. The error and
        invalid_channel events should be the only remaning.

        The connect signal is used for some setup such as faking
        channel subscription and removing any non-test event handlers
        since there's no way for the mock socketio object to know the
        format of the data they expect.
        """

        event_names = ["connect", "message", "invalid_channel", "disconnect",
                       "finish", "error"]

        @events.on_connect
        def test_connect(request, socket, context):
            for name in dir(events):
                event = getattr(events, name)
                if isinstance(event, events.Event):
                    event.handlers = [h for h in event.handlers
                                      if h[0].__name__.startswith("test_")]
            socket.channels.append("test")
            event_names.remove("connect")
            context["test1"] = 1
            context["test2"] = 2

        @events.on_message(channel="test")
        def test_message(request, socket, context, message):
            del context["test1"]
            event_names.remove("message")

        @events.on_message(channel="invalid_channel")
        def test_invalid_channel_message(request, socket, context, message):
            event_names.remove("invalid_channel")

        @events.on_disconnect(channel="test")
        def test_disconnect(request, socket, context):
            event_names.remove("disconnect")

        @events.on_finish(channel="test")
        def test_finish(request, socket, context):
            event_names.remove("finish")
            self.assertEqual(len(context), 1)
            self.assertTrue("test2" in context)

        @events.on_error(channel="test")
        def test_error(request, socket, context, exception):
            event_names.remove("error")

        response = SocketIoClient().get(reverse("socketio"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(event_names), 2)
        self.assertTrue("invalid_channel" in event_names)
        self.assertTrue("error" in event_names)
