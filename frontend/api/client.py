import httpx

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

class DeviceAPI:
    def __init__(self):
        self.base_uri = LITESTAR_BASE

    async def get_config(self):
        return await api_get("/api/config")

    async def restart(self):
        return await api_post("/api/restart")

    async def start_readings(self):
        return await api_get("/api/readings")
    
    async def get_api(self, endpoint):
        return await api_get(f"/api/{endpoint}")