
from django.http import HttpResponse

from django_socketio import events
from django_socketio.channels import SocketIOChannelProxy
from django_socketio.clients import client_start, client_end
from django_socketio.utils import format_log


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
    client_start(request, socket, context)
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
                    message = messages.next()
                    message_type = "subscribe"
                    socket.subscribe(message)
                    events.on_subscribe.send(request, socket, context, message)
                elif message == "__unsubscribe__":
                    message = messages.next()
                    message_type = "unsubscribe"
                    socket.unsubscribe(message)
                    events.on_unsubscribe.send(request, socket, context, message)
                else:
                    # Socket.IO sends arrays as individual messages, so
                    # they're put into an object in socketio_scripts.html
                    # and given the __array__ key so that they can be
                    # handled consistently in the on_message event.
                    message_type = "message"
                    if message == "__array__":
                        message = messages.next()
                    events.on_message.send(request, socket, context, message)
                log_message = format_log(request, message_type, message)
                if log_message:
                    socket.handler.server.log.write(log_message)
    except Exception, exception:
        from traceback import print_exc
        print_exc()
        events.on_error.send(request, socket, context, exception)
    client_end(request, socket, context)
    return HttpResponse("")
