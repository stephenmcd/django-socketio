Introduction
============

``django-socketio`` is a `BSD licensed`_ `Django`_ application that
brings together a variety of features that allow you to use
`websockets`_ seamlessly with any Django project.

``django-socketio`` was inspired by `Cody Soyland's`_ introductory
`blog post`_ on using `Socket.IO`_ and `gevent`_ with Django, and made
possible by the work of `Jeffrey Gelens'`_ `gevent-websocket`_ and
`gevent-socketio`_ packages.

The features provided by ``django-socketio`` are:

  * Installation of required packages from `PyPI`_
  * A management command for running gevent's pywsgi server with auto-reloading capabilities
  * A `signals`_-like event system that abstracts away the various stages of a Socket.IO request
  * A channel subscription and broadcast system that extends Socket.IO allowing websockets and events to be partitioned into separate concerns
  * The required views, urlpatterns, templatetags and tests for all the above

Installation
============

The easiest way install ``django-socketio`` is directly from PyPi using
`pip`_ or `setuptools`_ by running the respective command below, which
will also attempt to install the dependencies mentioned above::

    $ pip install -U django-socketio

or::

    $ easy_install -U django-socketio

Otherwise you can download ``django-socketio`` and install it directly
from source::

    $ python setup.py install

Once installed you can then add ``django_socketio`` to your
``INSTALLED_APPS`` and ``django_socketio.urls`` to your url conf.

Events
======

Channels
========

.. _`BSD licensed`: http://www.linfo.org/bsdlicense.html
.. _`Django`: http://djangoproject.com/
.. _`websockets`: http://en.wikipedia.org/wiki/WebSockets
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

