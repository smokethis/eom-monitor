import httpx
from shared.models.messages import ConfigMessage, InfoMessage
import msgspec

LITESTAR_BASE = "http://localhost:8000/"

class LitestarApiClient:
    def __init__(self):
        self.base_uri = LITESTAR_BASE
        self.http = httpx.AsyncClient(base_url=LITESTAR_BASE)

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
    
    # Generic endpoint getter, only really useful for debugging
    async def get_api(self, endpoint):
        return await self.http.get(f"/api{endpoint}")
