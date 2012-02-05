
from django.shortcuts import get_object_or_404
from django.utils.html import strip_tags
from django_socketio import events

from chat.models import ChatRoom


@events.on_message(channel="^room-")
def message(request, socket, context, message):
    """
    Event handler for a room receiving a message. First validates a
    joining user's name and sends them the list of users.
    """
    room = get_object_or_404(ChatRoom, id=message["room"])
    if message["action"] == "start":
        name = strip_tags(message["name"])
        user, created = room.users.get_or_create(name=name)
        if not created:
            socket.send({"action": "in-use"})
        else:
            context["user"] = user
            users = [u.name for u in room.users.exclude(id=user.id)]
            socket.send({"action": "started", "users": users})
            user.session = socket.session.session_id
            user.save()
            joined = {"action": "join", "name": user.name, "id": user.id}
            socket.send_and_broadcast_channel(joined)
    else:
        try:
            user = context["user"]
        except KeyError:
            return
        if message["action"] == "message":
            message["message"] = strip_tags(message["message"])
            message["name"] = user.name
            socket.send_and_broadcast_channel(message)


@events.on_finish(channel="^room-")
def finish(request, socket, context):
    """
    Event handler for a socket session ending in a room. Broadcast
    the user leaving and delete them from the DB.
    """
    try:
        user = context["user"]
    except KeyError:
        return
    left = {"action": "leave", "name": user.name, "id": user.id}
    socket.broadcast_channel(left)
    user.delete()
