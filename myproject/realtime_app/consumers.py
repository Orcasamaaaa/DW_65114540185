from channels.generic.websocket import AsyncWebsocketConsumer
import json
from clickhouse_connect import get_client
import asyncio


class EventConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        print("WebSocket connected!")  # Debug
        await self.accept()
        await self.send_current_count()

    async def disconnect(self, close_code):
        print(f"WebSocket disconnected: {close_code}")  # Debug

    async def receive(self, text_data):
        print(f"Received: {text_data}")  # Debug
        await self.send_current_count()

    async def send_current_count(self):
        def get_count():
            try:
                client = get_client(host='localhost', port=8123, username='default', password='')
                result = client.query('SELECT COUNT(*) FROM testdb.events')
                return result.result_rows[0][0]
            except Exception as e:
                print(f"ClickHouse error: {e}")
                return 0

        try:
            count = await asyncio.get_event_loop().run_in_executor(None, get_count)
            print(f"Sending count: {count}")  # Debug

            await self.send(text_data=json.dumps({
                'count': count
            }))
        except Exception as e:
            print(f"Send error: {e}")
            await self.send(text_data=json.dumps({
                'count': 0,
                'error': str(e)
            }))