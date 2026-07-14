import httpx
from ...shared.models.messages import ConfigMessage, InfoMessage
import msgspec
import websockets
import json

# from shared.models.messages import StreamMessage # This is pants and needs pants

LITESTAR_ADDRESS = "localhost:8000"
REST_BASE = (f"http://{LITESTAR_ADDRESS}")
WEBSOCKETS_BASE = (f"ws://{LITESTAR_ADDRESS}")

class LitestarApiClient:
    def __init__(self):
        self.http = httpx.AsyncClient(base_url=REST_BASE)
        self.websocket = None

    # RESTful endpoints
    async def get_info(self) -> InfoMessage:
        response = await self.http.get("/api/raw/info")
        return msgspec.convert(response.json(), type=InfoMessage)
    
    async def get_config(self) -> ConfigMessage:
        response = await self.http.get("/api/raw/config")
        return msgspec.convert(response.json(), type=ConfigMessage)

    async def restart(self) -> None:
        print("Someone POSTed to the restart endpoint!!!")
        await self.http.post("/api/restart")

    async def start_stream(self) -> None:
        await self.http.post("/api/start_stream")

    # Websockets endpoint
    async def connect_stream(self):
        self.websocket = await websockets.connect(
            f"{WEBSOCKETS_BASE}/api/stream"
        )

    async def disconnect_stream(self):
        if self.websocket:
            await self.websocket.close()
            self.websocket = None

    async def receive_stream_message(self):
        raw = await self.websocket.recv() # type: ignore

        # If your endpoint sends JSON text
        data = json.loads(raw)

        return data
