Introduction
============

django-socketio is a `BSD licensed`_ `Django`_ application that
brings together a variety of features that allow you to use
`WebSockets`_ seamlessly with any Django project.

django-socketio was inspired by `Cody Soyland's`_ introductory
`blog post`_ on using `Socket.IO`_ and `gevent`_ with Django, and
made possible by the work of `Jeffrey Gelens'`_ `gevent-websocket`_
and `gevent-socketio`_ packages.

The features provided by django-socketio are:

  * Installation of required packages from `PyPI`_
  * A management command for running gevent's pywsgi server with auto-reloading capabilities
  * A channel subscription and broadcast system that extends Socket.IO allowing WebSockets and events to be partitioned into separate concerns
  * A `signals`_-like event system that abstracts away the various stages of a Socket.IO request
  * The required views, urlpatterns, templatetags and tests for all the above

Installation
============

The easiest way install django-socketio is directly from PyPi using
`pip`_ or `setuptools`_ by running the respective command below, which
will also attempt to install the dependencies mentioned above::

    $ pip install -U django-socketio

or::

    $ easy_install -U django-socketio

Otherwise you can download django-socketio and install it directly
from source::

    $ python setup.py install

Once installed you can then add ``django_socketio`` to your
``INSTALLED_APPS`` and ``django_socketio.urls`` to your url conf. The
client-side JavaScripts for Socket.IO and its extensions can then be
added to any page with the ``socketio`` templatetag::

    <head>
        {% load socketio_tags %}
        {% socketio %}
        <script>
            var socket = new io.Socket();
            socket.connect();
            // etc
        </script>
    </head>

Running
=======

The ``runserver_socketio`` management command is provided which will
run gevent's pywsgi server which is required for supporting the type of
long-running request a WebSocket will use::

    $ python manage.py runserver_socketio addr:port

Channels
========

The WebSocket implemented by gevent-websocket provides two methods for
sending data to other clients, ``socket.send`` which sends data to the
given socket instance, and ``socket.broadcast`` which sends data to all
socket instances other than itself.

A common requirement for WebSocket based applications is to divide
communications up into separate channels. For example a chat site may
have multiple chat rooms and rather than using ``broadcast`` which
would send a chat message to all chat rooms, each room would need a
reference to each of the connected sockets so that ``send`` can be
called on each socket when a new message arrives for that room.

django-socketio extends Socket.IO both on the client and server to
provide channels that can be subscribed and broadcast to.

To subscribe to a channel client-side in JavaScript use the
``socket.subscribe`` method::

    var socket = new io.Socket();
    socket.connect();
    socket.on('connect', function() {
        socket.subscribe('my channel');
    });

Once the socket is subscribed to a channel, you can then
broadcast to the channel server-side in Python using the
``socket.broadcast_channel`` method::

  socket.broadcast_channel("my message")

Events
======

The ``django_socketio.events`` module provides a handful of events
that can be subscribed to, very much like connecting receiver
functions to Django signals. Each of these events are raised
throughout the relevant stages of a Socket.IO request.

Events are subscribed to by applying each event as a decorator
to your event handler functions::

    from django_socketio.events import on_message

    @on_message
    def my_message_handler(request, socket, message):
        ...

Each event handler takes at least two arguments: the current Django
``request``, and the Socket.IO ``socket`` the event occurred for.

  * ``on_connect`` - occurs once when the WebSocket connection is first established.
  * ``on_message`` - occurs every time data is sent to the WebSocket. Takes a third ``message`` argument which contains the data sent.
  * ``on_subscribe`` - occurs when a channel is subscribed to. Takes a third ``channel`` argument which contains the channel subscribed to.
  * ``on_unsubscribe`` - occurs when a channel is unsubscribed from. Takes a third ``channel`` argument which contains the channel unsubscribed from.
  * ``on_error`` - occurs when an error is raised. Takes a third ``exception`` argument which contains the exception for the error.
  * ``on_disconnect`` - occurs once when the WebSocket disconnects.
  * ``on_finish`` - occurs once when the Socket.IO request is finished.

Like Django signals, event handlers can be defined anywhere so long
as they end up being imported. Consider adding them to their own
module that gets imported by your urlconf, or even adding them to
your views module since they're conceptually similar to views.

Binding Events to Channels
==========================

All events other than the ``on_connect`` event can also be bound to
particular channels by passing a ``channel`` argument to the event
decorator. The channel argument can contain a regular expression
pattern used to match again multiple channels of similar function.

For example, suppose you implemented a chat site with multiple rooms.
WebSockets would be the basis for users communicating within each
chat room, however you may want to use them elsewhere throughout the
site for different purposes, perhaps for a real-time admin dashboard.
In this case there would be two distinct WebSocket uses, with the chat
rooms each requiring their own individual channels.

Suppose each chat room user subscribes to a channel client-side
using the room's ID::

    var socket = new io.Socket();
    var roomID = 42;
    socket.connect();
    socket.on('connect', function() {
        socket.subscribe('room-' + roomID);
    });

Then server-side the different message handlers are bound to each
type of channel::

    @on_message(channel="dashboard")
    def my_dashboard_handler(request, socket, message):
        ...

    @on_message(channel="^room-")
    def my_chat_handler(request, socket, message):
        ...

Chat Demo
=========

The "hello world" of WebSocket applications is naturally the chat
room. As such django-socketio comes with a demo chat application
that provides examples of the different events and channel features
available. The demo can be found in the ``example_project`` directory
of the ``django_socketio`` package. Note that Django 1.3 or higher
is required for the demo as it makes use of Django 1.3's
``staticfiles`` app.

.. _`BSD licensed`: http://www.linfo.org/bsdlicense.html
.. _`Django`: http://djangoproject.com/
.. _`WebSockets`: http://en.wikipedia.org/wiki/WebSockets
.. _`Cody Soyland's`: http://codysoyland.com/
.. _`blog post`: http://codysoyland.com/2011/feb/6/evented-django-part-one-socketio-and-gevent/
.. _`Socket.IO`: http://socket.io/
.. _`Jeffrey Gelens'`: http://www.gelens.org/
.. _`gevent`: http://www.gevent.org/
.. _`gevent-websocket`: https://bitbucket.org/Jeffrey/gevent-websocket/
.. _`gevent-socketio`: https://bitbucket.org/Jeffrey/gevent-socketio/
.. _`PyPI`: http://pypi.python.org/
.. _`signals`: https://docs.djangoproject.com/en/dev/topics/signals/
.. _`pip`: http://www.pip-installer.org/
.. _`setuptools`: http://pypi.python.org/pypi/setuptools
