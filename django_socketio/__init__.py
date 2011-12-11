
__version__ = "0.2"


class NoSockets(Exception):
    """
    Raised when no clients are available to broadcast to.
    """


def broadcast(message):
    """
    Find the first socket and use it to broadcast to all sockets
    including the socket itself.
    """
    from django_socketio.views import CLIENTS
    try:
        socket = CLIENTS.values()[0][1]
    except IndexError:
        raise NoSockets("There are no clients.")
    socket.send_and_broadcast(message)


def broadcast_channel(message, channel):
    """
    Find the first socket for the given channel, and use it to
    broadcast to the channel, including the socket itself.
    """
    from django_socketio.views import CLIENTS
    from django_socketio.channels import CHANNELS
    try:
        first_session_for_channel = CHANNELS.get(channel, [])[0]
    except IndexError:
        raise NoSockets()
    else:
        for (request, socket, context) in CLIENTS.values():
            if socket.session.session_id == first_session_for_channel:
                break
        else:
            raise NoSockets("There are no clients on the channel: " + channel)
    socket.send_and_broadcast_channel(message, channel)
