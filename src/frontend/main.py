from nicegui import ui
from frontend.ui.routes import register_routes
from frontend.api.client import LitestarApiClient
from frontend.services.device_service import DeviceService

client = LitestarApiClient()
service = DeviceService(client)

register_routes(client, service)

ui.run(
    host="0.0.0.0",
    port=8080
)