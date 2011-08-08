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
  * A channel subscription and broadcast system that extends Socket.IO allowing websockets and events to be partitioned into separate concerns
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
``INSTALLED_APPS`` and ``django_socketio.urls`` to your url conf.

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

The ``django_socket.io.events`` module provides a handful of events
that can be subscribed to, very much like connecting receiver
functions to Django signals.

TODO: document each event


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

