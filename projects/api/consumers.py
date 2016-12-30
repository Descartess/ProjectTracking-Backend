#consumers.py
from channels import Group 

def ws_connect(message):
	Group("logs").add(message.reply_channel)

def ws_disconnect(message):
	Group("logs").discard(message.reply_channel)
