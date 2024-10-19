import logging
import json
from channels.generic.websocket import AsyncWebsocketConsumer


class DLRConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.group_name = "dlr_updates"

        # Log connection event
        logging.info(f"WebSocket connection established with {self.channel_name}")

        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        logging.info(f"WebSocket disconnected: {close_code}")

        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    # Receive message from room group
    async def dlr_message(self, event):
        message = event["message"]

        # Log message received
        logging.info(f"WebSocket received message: {message}")

        # Send message to WebSocket
        await self.send(text_data=json.dumps({"message": message}))
