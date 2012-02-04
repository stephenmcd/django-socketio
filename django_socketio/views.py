
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
            messages = socket.recv()
            if not messages and not socket.connected():
                events.on_disconnect.send(request, socket, context)
                break
            # Subscribe and unsubscribe messages are in two parts, the
            # name of either and the channel, so we use an iterator that
            # lets us jump a step in iteration to grab the channel name
            # for these.
            messages = iter(messages)
            for message in messages:
                if message == "__subscribe__":
                    chan = messages.next()
                    socket.subscribe(chan)
                    events.on_subscribe.send(request, socket, context, chan)
                    message = "[subscribe] %s" % chan
                elif message == "__unsubscribe__":
                    chan = messages.next()
                    socket.unsubscribe(chan)
                    events.on_unsubscribe.send(request, socket, context, chan)
                    message = "[unsubscribe] %s" % chan
                else:
                    # Socket.IO transfers arrays as individual messages, so
                    # they're put into an object in socketio_scripts.html
                    # and given the __array__ key so that they can be treated
                    # consistently here.
                    if message == "__array__":
                        message = messages.next()
                    events.on_message.send(request, socket, context, message)
                if MESSAGE_LOG_FORMAT is not None:
                    formatted = format_log(request, message)
                    socket.handler.server.log.write(formatted)
    except Exception, exception:
        print_exc()
        events.on_error.send(request, socket, context, exception)
    # Send the unsubscribe event prior to actually unsubscribing, so
    # that the finish event can still match channels if applicable.
    for channel in socket.channels:
        events.on_unsubscribe.send(request, socket, context, channel)
    events.on_finish.send(request, socket, context)
    # Actually unsubscribe to cleanup channel data.
    for channel in socket.channels:
        socket.unsubscribe(channel)
    del CLIENTS[socket.session.session_id]
    return HttpResponse("")
