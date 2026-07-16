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

app.colors(
    primary = '#5898d4',
    secondary = '#26a69a',
    accent = '#9c27b0',
    dark = '#1d1d1d',
    dark_page = '#121212',
    positive = '#21ba45',
    negative = '#c10015',
    info = '#31ccec',
    warning = '#f2c037'
    # Add additional custom colours with 'name' = 'hex
    )

register_routes(client, service)

ui.run(
    host="0.0.0.0",
    port=8080,
    reload=False # Needed for debugging
)