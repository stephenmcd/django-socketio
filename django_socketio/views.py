
from atexit import register
from datetime import datetime
from traceback import print_exc

from django.http import HttpResponse

from django_socketio import events
from django_socketio.channels import SocketIOChannelProxy
from django_socketio.settings import MESSAGE_LOG_FORMAT


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
    for client in CLIENTS.values():
        events.on_finish.send(*client)

def format_log(request, message):
    """
    Formats a log message similar to gevent's pywsgi request logging.
    """
    now = datetime.now().replace(microsecond=0)
    log = MESSAGE_LOG_FORMAT % dict(request.META, MESSAGE=message, TIME=now)
    return log + "\n"

def socketio(request):
    """
    Socket.IO handler - maintains the lifecycle of a Socket.IO
    request, sending the each of the events. Also handles
    adding/removing request/socket pairs to the CLIENTS dict
    which is used for sending on_finish events when the server
    stops.
    """
    context = {}
    socket = SocketIOChannelProxy(request.environ["socketio"])
    CLIENTS[socket.session.session_id] = (request, socket, context)
    try:
        if socket.on_connect():
            events.on_connect.send(request, socket, context)
        while True:
            message = socket.recv()
            if len(message) > 0:
                if MESSAGE_LOG_FORMAT is not None:
                    socket.handler.server.log.write(format_log(request, message))

                # Handle subscribe and unsubscribe requests, then excise
                # them from the message.
                to_remove = []
                for i in range(0, len(message)-1):
                    if message[i] == "__subscribe__":
                        socket.subscribe(message[i+1])
                        events.on_subscribe.send(request, socket, context, message[i+1])
                        to_remove += [i, i+1]
                    elif message[i] == "__unsubscribe__":
                        events.on_unsubscribe.send(request, socket, context, message[i+1])
                        socket.unsubscribe(message[i+1])
                        to_remove += [i, i+1]
                to_remove.reverse()
                for index in to_remove: message.pop(index)

                if len(message) > 0:
                    events.on_message.send(request, socket, context, message)
            else:
                if not socket.connected():
                    events.on_disconnect.send(request, socket, context)
                    break
    except Exception, exception:
        print_exc()
        events.on_error.send(request, socket, context, exception)
    events.on_finish.send(request, socket, context)
    del CLIENTS[socket.session.session_id]
    return HttpResponse("")
