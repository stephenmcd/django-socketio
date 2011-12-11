
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import get_object_or_404, render, redirect
from django.utils.html import strip_tags
from django_socketio import events, broadcast, broadcast_channel, NoSockets

from chat.models import ChatRoom, ChatUser


@events.on_message(channel="^room-")
def message(request, socket, context, message):
    """
    Event handler for a room receiving a message. First validates a
    joining user's name and sends them the list of users.
    """
    message = message[0]
    room = get_object_or_404(ChatRoom, id=message["room"])
    if message["action"] == "start":
        user, created = room.users.get_or_create(name=strip_tags(message["name"]))
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
    socket.broadcast_channel({"action": "leave", "name": user.name, "id": user.id})
    user.delete()

def rooms(request, template="rooms.html"):
    """
    Homepage - lists all rooms.
    """
    context = {"rooms": ChatRoom.objects.all()}
    return render(request, template, context)

def room(request, slug, template="room.html"):
    """
    Show a room.
    """
    context = {"room": get_object_or_404(ChatRoom, slug=slug)}
    return render(request, template, context)

def create(request):
    """
    Handles post from the "Add room" form on the homepage, and
    redirects to the new room.
    """
    name = request.POST.get("name")
    if name:
        room, created = ChatRoom.objects.get_or_create(name=name)
        return redirect(room)
    return redirect(rooms)

@user_passes_test(lambda user: user.is_staff)
def system_message(request, template="system_message.html"):
    context = {"rooms": ChatRoom.objects.all()}
    if request.method == "POST":
        room = request.POST["room"]
        data = {"action": "system", "message": request.POST["message"]}
        try:
            if room:
                broadcast_channel(data, channel="room-" + room)
            else:
                broadcast(data)
        except NoSockets, e:
            context["message"] = e
        else:
            context["message"] = "Message sent"
    return render(request, template, context)
