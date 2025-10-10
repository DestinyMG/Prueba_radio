from channels.generic.websocket import AsyncWebsocketConsumer

class StreamingConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_group_name = "streaming_room"

        # Añadir cliente al grupo
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()
        print("Cliente conectado al WebSocket")

    async def disconnect(self, close_code):
        # Quitar cliente del grupo
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
        print("Cliente desconectado del WebSocket")

    async def receive(self, text_data=None, bytes_data=None):
        # Reenviar a todos los clientes del grupo (Transmitter y Receiver)
        if bytes_data:
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    "type": "broadcast_audio",
                    "bytes_data": bytes_data,
                }
            )

    async def broadcast_audio(self, event):
        # Enviar el audio a todos los clientes conectados
        bytes_data = event["bytes_data"]
        await self.send(bytes_data=bytes_data)
        print("Audio enviado a los clientes")