
from django.core.handlers.base import BaseHandler
from django.core.handlers.wsgi import WSGIRequest
from django.core.urlresolvers import reverse
from django.test import Client
from django.test import TestCase


class MockSocketIoClient(Client):
    """
    Mocks a socket.io request for testing.
    """
    def request(self, **request):

        class MockSocketIo(object):

            def on_connect(self):
                return True
            def recv(self):
                return ""
            def connected(self):
                return False

        environ = {
            'HTTP_COOKIE': self.cookies,
            'PATH_INFO': '/',
            'QUERY_STRING': '',
            'REQUEST_METHOD': 'GET',
            'SCRIPT_NAME': '',
            'SERVER_NAME': 'testserver',
            'SERVER_PORT': 80,
            'SERVER_PROTOCOL': 'HTTP/1.1',
            'socketio': MockSocketIo()
        }

        environ.update(self.defaults)
        environ.update(request)
        request = WSGIRequest(environ)
        handler = BaseHandler()
        handler.load_middleware()
        for middleware_method in handler._request_middleware:
            if middleware_method(request):
                raise Exception("Couldn't create request object - "
                                "request middleware returned a response")

        return request

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
