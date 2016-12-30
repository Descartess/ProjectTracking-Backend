#asgi.py
import os
import channels.asgi

oe.environ.setdefault("DJANGO_SETTINGS_MODULE","proj_track.settings")

channel_layer = channels.asgi.get_channel_layer()