from channels.generic.websocket import AsyncWebsocketConsumer
import json


class MyConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        print("Hello")
        await self.accept()
        await self.send(text_data=json.dumps("Helllo"))

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        await self.send(text_data=json.dumps(f"Received: {text_data}"))
        pass
