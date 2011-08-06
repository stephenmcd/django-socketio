
from atexit import register

from datetime import datetime
from traceback import print_exc

from django.http import HttpResponse

from django_socketio import signals
from django_socketio.channels import ChanneledSocketIOProtocol

# Maps open Socket.IO session IDs to request/socket pairs for
# guaranteeing the on_finish signal being sent when the server
# stops.
CLIENTS = {}

@register
def cleanup():
    """
    Sends the on_finish signal to any open clients when the server
    is unexpectedly stopped.
    """
    for request, socket in CLIENTS.values():
        signals.on_finish.send(sender=request, socket=socket)

def format_log(request, message):
    """
    Formats a log message similar to gevent's pywsgi request logging.
    """
    now = datetime.now().replace(microsecond=0)
    info = (request.META["REMOTE_ADDR"], now, message)
    return '%s - - [%s] "Socket.IO message: %s"' % info

def socketio(request):
    """
    Socket.IO handler - maintains the lifecycle of a Socket.IO
    connection, sending the each of the signals. Also handles
    adding/removing request/socket pairs to the CLIENTS dict
    which is used for sending on_finish signals when the server
    stops.
    """
    socket = ChanneledSocketIOProtocol(request.environ["socketio"])
    CLIENTS[socket.session.session_id] = (request, socket)
    signal_args = {"sender": request, "socket": socket}
    if socket.on_connect():
        signals.on_connect.send(**signal_args)
    try:
        while True:
            message = socket.recv()
            if len(message) > 0:
                socket.log(format_log(request, message))
                if message[0] == "__subscribe__" and len(message) == 2:
                    socket.subscribe(message[1])
                    signals.on_subscribe.send(channel=message[1], **signal_args)
                elif message[0] == "__unsubscribe__" and len(message) == 2:
                    socket.unsubscribe(message[1])
                    signals.on_unsubscribe.send(channel=message[1], **signal_args)
                else:
                    signals.on_message.send(message=message, **signal_args)
            else:
                if not socket.connected():
                    signals.on_disconnect.send(**signal_args)
                    break
    except Exception, e:
        print_exc()
        signals.on_error.send(exception=e, **signal_args)
    signals.on_finish.send(**signal_args)
    del CLIENTS[socket.session.session_id]
    return HttpResponse("")
