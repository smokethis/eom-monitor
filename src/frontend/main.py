from nicegui import ui, app
import asyncio
from src.frontend.ui.routes import register_routes
from src.frontend.api.client import LitestarApiClient
from src.frontend.services.device_service import DeviceService
import logging

client = LitestarApiClient()
service = DeviceService(client)

logging.basicConfig(level=logging.DEBUG)
# logging.basicConfig(level=logging.INFO)

@app.on_startup
async def startup():
    asyncio.create_task(service.start())

register_routes(client, service)

ui.run(
    host="0.0.0.0",
    port=8080,
    reload=False # Needed for debugging
)