
from django.dispatch import receiver
from django.shortcuts import get_object_or_404, render
from django.utils.html import strip_tags
from django_socketio import signals

from chat.models import ChatRoom, ChatUser


@receiver(signals.on_message)
def message(request=None, socket=None, message=None, **kwargs):
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
            socket.send({"action": "start", "users": users})
            socket.broadcast_channel({"action": "join", "user": user.name})
    else:
        try:
            user = room.users.get(session=socket.session.session_id)
        except ChatUser.DoesNotExist:
            return
        if message["action"] == "message":
            message["message"] = strip_tags(message["message"])
            message["user"] = user.name
            socket.send(message)
            socket.broadcast_channel(message)

@receiver(signals.on_finish)
def finish(request=None, socket=None, **kwargs):
    try:
        user = ChatUser.objects.get(session=socket.session.session_id)
    except ChatUser.DoesNotExist:
        return
    socket.broadcast_channel({"action": "leave", "user": user.name})
    user.delete()


def rooms(request, template="rooms.html"):
    context = {"rooms": ChatRoom.objects.all()}
    return render(request, template, context)

def room(request, slug, template="room.html"):
    context = {"room": get_object_or_404(ChatRoom, slug=slug)}
    return render(request, template, context)
