
from atexit import register

from datetime import datetime
from traceback import print_exc

from django.http import HttpResponse

from django_socketio import signals
from django_socketio.channels import ChanneledSocketIOProtocol


CLIENTS = {}

@register
def cleanup():
    for request, socket in CLIENTS.values():
        signals.on_finish.send(sender=request, socket=socket)

def socketio(request):
    """
    Socket.IO handler.
    """
    socket = ChanneledSocketIOProtocol(request.environ["socketio"])
    CLIENTS[socket.session.session_id] = (request, socket)
    if socket.on_connect():
        signals.on_connect.send(sender=request, socket=socket)
    try:
        while True:
            message = socket.recv()
            if len(message) > 0:
                now = datetime.now().replace(microsecond=0)
                info = (request.META["REMOTE_ADDR"], now, message)
                socket.log('%s - - [%s] "Socket.IO message: %s"' % info)
                if message[0] == "__subscribe__" and len(message) == 2:
                    socket.subscribe(message[1])
                    signals.on_subscribe.send(sender=request, socket=socket, channel=message[1])
                elif message[0] == "__unsubscribe__" and len(message) == 2:
                    socket.unsubscribe(message[1])
                    signals.on_unsubscribe.send(sender=request, socket=socket, channel=message[1])
                else:
                    signals.on_message.send(sender=request, socket=socket, message=message)
            else:
                if not socket.connected():
                    signals.on_disconnect.send(sender=request, socket=socket)
                    break
    except Exception, e:
        print_exc()
        signals.on_error.send(sender=request, socket=socket, exception=e)
    signals.on_finish.send(sender=request, socket=socket)
    del CLIENTS[socket.session.session_id]
    return HttpResponse("")
