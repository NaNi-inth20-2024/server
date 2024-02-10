from channels.generic.websocket import AsyncWebsocketConsumer


class MyConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        print("Hello")
        await self.accept()

    async def disconnect(self, close_code):
        pass

    async def receive(selfl, text_data):
        pass
