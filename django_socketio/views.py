
from django.http import HttpResponse

from django_socketio import signals


def socketio(request):
    """
    Socket.IO handler.
    """
    socket = request.environ["socketio"]
    if socket.on_connect():
        signals.on_connect.send(sender=request, socket=socket)
    try:
        while True:
            message = socket.recv()
            if len(message) > 0:
                signals.on_message.send(sender=request, socket=socket, message=message)
            else:
                if not socket.connected():
                    signals.on_disconnect.send(sender=request, socket=socket)
                    break
    except Exception, e:
        signals.on_error.send(sender=request, socket=socket, exception=e)
    signals.on_finish.send(sender=request, socket=socket)
    return HttpResponse("")
