#routing.py

from channels import route
from projects.api.consumers import *

channel_routing = [
	route("websocket.connect",ws_connect),
	route("websocket.disconnect",ws_disconnect)
]

