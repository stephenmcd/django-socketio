
__version__ = "0.2.3"


class NoSocket(Exception):
    """
    Raised when no clients are available to broadcast to.
    """


def send(session_id, message):
    """
    Send a message to the socket for the given session ID.
    """
    from django_socketio.clients import CLIENTS
    try:
        socket = CLIENTS[session_id][1]
    except KeyError:
        raise NoSocket("There is no socket with the session ID: " + session_id)
    socket.send(message)


def broadcast(message):
    """
    Find the first socket and use it to broadcast to all sockets
    including the socket itself.
    """
    from django_socketio.clients import CLIENTS
    try:
        socket = CLIENTS.values()[0][1]
    except IndexError:
        raise NoSocket("There are no clients.")
    socket.send_and_broadcast(message)


def broadcast_channel(message, channel):
    """
    Find the first socket for the given channel, and use it to
    broadcast to the channel, including the socket itself.
    """
    from django_socketio.clients import CLIENTS
    from django_socketio.channels import CHANNELS
    try:
        socket = CLIENTS[CHANNELS.get(channel, [])[0]][1]
    except IndexError, KeyError:
        raise NoSocket("There are no clients on the channel: " + channel)
    socket.send_and_broadcast_channel(message, channel)
