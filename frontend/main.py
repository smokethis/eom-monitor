from nicegui import ui
from ui.routes import register_routes
from api.client import Client
from device.models import Device
from services.device_service import DeviceService

async def main():
    client = Client()
    device = Device()
    service = DeviceService(client, device)

    await service.start()

    register_routes(device)

    ui.run(
        host="0.0.0.0",
        port=8080
    )