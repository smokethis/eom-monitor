from litestar import Litestar
from litestar.di import Provide
from .api import routes
from .eom.websocketclient import Client
from .eom.serialclient import SerialReader
from ..shared.device.device import Device, DeviceRaw
from .services.device_service import DeviceService
from .services.device_bus import DeviceEventBus
import logging
import asyncio
import os
from contextlib import asynccontextmanager

# Set this when debugging. Save me from stupid software
logging.basicConfig(level=logging.DEBUG)
# logging.basicConfig(level=logging.INFO)

eom_ip = os.environ["EOM_IP"]
eom_port = int(os.environ["EOM_PORT"])

# client = Client(ip=eom_ip, port=eom_port)
device = Device()
event_bus = DeviceEventBus()
raw = DeviceRaw()
# service = DeviceService(client, device, raw, event_bus)x
client = SerialReader("/dev/tty.usbserial-DU0DI6KU", 115200)

@asynccontextmanager
async def lifespan(app: Litestar):

    print("Starting application")
    # if not client.port_probe():
        # raise RuntimeError("Device unavailable")
    
    # Yes, really; start these tasks and proceed
    client_task = asyncio.create_task(client.run())
    # service_task = asyncio.create_task(service.run())

    # Wait for shutdown to commence
    yield

    # Run shutdown tasks
    print("Stopping application")
    # await service.close()

    client_task.cancel()
    # service_task.cancel()

    await asyncio.gather(
        client_task,
        # service_task,
        return_exceptions=True,
    )

# Litestar app configuration
app = Litestar(
    route_handlers=[
        routes.get_config, 
        routes.get_readings,
        routes.get_readings_history,
        routes.restart_device,
        routes.start_stream,
        routes.get_info,
        routes.update_config,
        routes.update_info,
        routes.stream,
        # set_mode, 
        # set_motor_speed,
        # set_config
    ],
    lifespan=[lifespan],
    dependencies={
        # "service": Provide(lambda: service, sync_to_thread=False),
        # "event_bus": Provide(lambda: service.event_bus, sync_to_thread=False)
    }
)