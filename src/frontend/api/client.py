import httpx
from shared.models.messages import ConfigMessage, InfoMessage

LITESTAR_BASE = "http://localhost:8000/"

class LitestarApiClient:
    def __init__(self):
        self.base_uri = LITESTAR_BASE
        self.http = httpx.AsyncClient(base_url=LITESTAR_BASE)

    async def get_info(self) -> InfoMessage:
        response = await self.http.get("/api/raw/info")
        return InfoMessage(**response.json())
    
    async def get_config(self) -> ConfigMessage:
        response = await self.http.get("/api/raw/config")
        return ConfigMessage(**response.json())

    async def restart(self) -> None:
        print("Someone POSTed to the restart endpoint!!!")
        await self.http.post("/api/restart")

    async def start_stream(self) -> None:
        await self.http.post("/api/start_stream")
    
    # Generic endpoint getter, only really useful for debugging
    async def get_api(self, endpoint):
        return await self.http.get(f"/api{endpoint}")


# # Generic API GET function
# async def api_get(path):
#     async with httpx.AsyncClient() as client:
#         response = await client.get(f"{LITESTAR_BASE}{path}")

#         if response.is_error:
#             return {
#                 "status": response.status_code,
#                 "error": response.text
#             }

#         return response.json()

# # Generic API POST function
# async def api_post(self, path):
#     response = await self.post(path)

#     if response.is_error:
#         return {
#             "status": response.status_code,
#             "error": response.text
#         }

    # async def get_config(self) -> ConfigMessage:
    #     data = await api_get("/api/raw/config")
    #     return ConfigMessage(**data)

    # async def get_info(self) -> InfoMessage:
    #     data = await api_get("/api/raw/config")
    #     return InfoMessage(**data)