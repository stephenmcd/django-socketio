
from django.shortcuts import get_object_or_404, render
from django.utils.html import strip_tags
from django_socketio import events

from chat.models import ChatRoom, ChatUser


@events.on_message(channel="^room-")
def message(request, socket, message):
    message = message[0]
    room = get_object_or_404(ChatRoom, id=message["room"])
    if message["action"] == "start":
        user, created = room.users.get_or_create(name=strip_tags(message["name"]))
        if not created:
            socket.send({"action": "in-use"})
        else:
            user.session = socket.session.session_id
            user.save()
            users = [u.name for u in room.users.all()]
            socket.send({"action": "started", "users": users})
            socket.broadcast_channel({"action": "join", "name": user.name})
    else:
        try:
            user = room.users.get(session=socket.session.session_id)
        except ChatUser.DoesNotExist:
            return
        if message["action"] == "message":
            message["message"] = strip_tags(message["message"])
            message["name"] = user.name
            socket.send(message)
            socket.broadcast_channel(message)

@events.on_finish(channel="^room-")
def finish(request, socket):
    try:
        user = ChatUser.objects.get(session=socket.session.session_id)
    except ChatUser.DoesNotExist:
        return
    socket.broadcast_channel({"action": "leave", "name": user.name})
    user.delete()

def rooms(request, template="rooms.html"):
    context = {"rooms": ChatRoom.objects.all()}
    return render(request, template, context)

def room(request, slug, template="room.html"):
    context = {"room": get_object_or_404(ChatRoom, slug=slug)}
    return render(request, template, context)
