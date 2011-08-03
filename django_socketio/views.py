
from django.http import HttpResponse

from django_socketio import signals
from django_socketio.channels import ChanneledSocketIOProtocol


def socketio(request):
    """
    Socket.IO handler.
    """
    socket = ChanneledSocketIOProtocol(request.environ["socketio"])
    if socket.on_connect():
        signals.on_connect.send(sender=request, socket=socket)
    try:
        while True:
            message = socket.recv()
            if len(message) > 0:
                print "ya"
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
        print e
        signals.on_error.send(sender=request, socket=socket, exception=e)
    signals.on_finish.send(sender=request, socket=socket)
    return HttpResponse("")
