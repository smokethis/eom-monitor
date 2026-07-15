from litestar import Litestar
from litestar.di import Provide
from .api import routes
from .eom.websocketclient import WebClient
from .eom.serialclient import SerialClient
from ..shared.device.device import Device, DeviceRaw
from .services.device_service import DeviceService
from .services.device_bus import DeviceEventBus
import logging
import asyncio
import os
from contextlib import asynccontextmanager

# Set this when debugging. Save me from stupid software
# logging.basicConfig(level=logging.DEBUG)
logging.basicConfig(level=logging.INFO)

eom_ip = os.environ["EOM_IP"]
eom_port = int(os.environ["EOM_PORT"])
eom_serial = os.environ["EOM_SERIAL"]

webclient = WebClient(ip=eom_ip, port=eom_port)
serialclient = SerialClient(eom_serial, 115200)
device = Device()
event_bus = DeviceEventBus()
raw = DeviceRaw()
service = DeviceService(webclient, serialclient, device, raw, event_bus)

@asynccontextmanager
async def lifespan(app: Litestar):

    if not webclient.port_probe():
        raise RuntimeError("Device unavailable")
    
    # Yes, really; start these tasks and proceed
    serial_client_task = asyncio.create_task(serialclient.run())
    web_client_task = asyncio.create_task(webclient.run())
    service_task = asyncio.create_task(service.run())

    # Wait for shutdown to commence
    yield

    # Run shutdown tasks
    print("Stopping application")
    await service.close()

    serial_client_task.cancel()
    web_client_task.cancel()
    service_task.cancel()

    await asyncio.gather(
        serial_client_task,
        web_client_task,
        service_task,
        return_exceptions=True
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
        "service": Provide(lambda: service, sync_to_thread=False),
        "event_bus": Provide(lambda: service.event_bus, sync_to_thread=False)
    }
)