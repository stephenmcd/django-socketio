
from re import match
from thread import start_new_thread
from time import sleep
from os import getpid, kill
from signal import SIGINT

from django.core.handlers.wsgi import WSGIHandler
from django.core.management.base import BaseCommand, CommandError
from django.core.management.commands.runserver import naiveip_re
from django.utils.autoreload import code_changed, restart_with_reloader
from socketio import SocketIOServer


RELOAD = False

def reload_watcher():
    global RELOAD
    while True:
        RELOAD = code_changed()
        if RELOAD:
            kill(getpid(), SIGINT)
        sleep(1)

class Command(BaseCommand):

    def handle(self, addrport="", **kwargs):

        if not addrport:
            self.addr = "127.0.0.1"
            self.port = 9000
        else:
            m = match(naiveip_re, addrport)
            if m is None:
                raise CommandError('"%s" is not a valid port number '
                                   'or address:port pair.' % addrport)
            self.addr, _, _, _, self.port = m.groups()

        start_new_thread(reload_watcher, ())
        try:
            bind = (self.addr, int(self.port))
            print
            print "SocketIOServer running on %s:%s" % bind
            print
            server = SocketIOServer(bind, WSGIHandler(), resource="socket.io")
            server.serve_forever()
        except KeyboardInterrupt:
            if RELOAD:
                print
                print "Reloading..."
                restart_with_reloader()
            else:
                raise
