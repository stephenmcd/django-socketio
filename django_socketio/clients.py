
from django_socketio import events


# Maps open Socket.IO session IDs to request/socket pairs for
# running cleanup code and events when the server is shut down
# or reloaded.
CLIENTS = {}


def client_start(request, socket, context):
    """
    Adds the client triple to CLIENTS.
    """
    CLIENTS[socket.session.session_id] = (request, socket, context)


def client_end(request, socket, context):
    """
    Handles cleanup when a session ends for the given client triple.
    Sends unsubscribe and finish events, actually unsubscribes from
    any channels subscribed to, and removes the client triple from
    CLIENTS.
    """
    # Send the unsubscribe event prior to actually unsubscribing, so
    # that the finish event can still match channels if applicable.
    for channel in socket.channels:
        events.on_unsubscribe.send(request, socket, context, channel)
    events.on_finish.send(request, socket, context)
    # Actually unsubscribe to cleanup channel data.
    for channel in socket.channels:
        socket.unsubscribe(channel)
    # Remove the client.
    del CLIENTS[socket.session.session_id]


def client_end_all():
    """
    Performs cleanup on all clients - called by runserver_socketio
    when the server is shut down or reloaded.
    """
    for request, socket, context in list(CLIENTS.values()):
        client_end(request, socket, context)


