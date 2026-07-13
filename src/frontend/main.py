from nicegui import ui, app
import asyncio
from frontend.ui.routes import register_routes
from frontend.api.client import LitestarApiClient
from frontend.services.device_service import DeviceService

client = LitestarApiClient()
service = DeviceService(client)

@app.on_startup
async def startup():
    asyncio.create_task(service.start())

register_routes(client, service)

ui.run(
    host="0.0.0.0",
    port=8080
)