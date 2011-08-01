
from django.http import HttpResponse


def socketio(request):
    """
    Socket.IO handler.
    """
    socket = request.environ["socketio"]
    if socketio.on_connect():
        # connect - request, socket
    try:
        while True:
            message = socket.recv()
            if len(message) > 0:
                # receive - request, socket, message
            else:
                if not socket.connected():
                    # disconnect - request, socket
                    break
    except Exception, e:
        # error - request, socket, exception
    # end - request, socket
    return HttpResponse("")
