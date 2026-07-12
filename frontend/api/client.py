import httpx
from .models import Info, Config

LITESTAR_BASE = "http://localhost:8000/"

# Generic API GET function
async def api_get(path):
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{LITESTAR_BASE}{path}")

        if response.is_error:
            return {
                "status": response.status_code,
                "error": response.text
            }

        return response.json()

# Generic API POST function
async def api_post(path):
    async with httpx.AsyncClient() as client:
        response = await client.post(f"{LITESTAR_BASE}{path}")

        if response.is_error:
            return {
                "status": response.status_code,
                "error": response.text
            }

class Client:
    def __init__(self):
        self.base_uri = LITESTAR_BASE

    async def get_config(self) -> Config:
        data = await api_get("/api/config")
        return Config(**data)

    async def get_info(self) -> Info:
        data = await api_get("/api/config")
        return Info(**data)

    async def restart(self) -> None:
        await api_post("/api/restart")

    async def start_stream(self) -> None:
        await api_post("/api/start_stream")
    
    # Generic endpoint getter, only really useful for debugging
    async def get_api(self, endpoint):
        return await api_get(f"/api/{endpoint}")