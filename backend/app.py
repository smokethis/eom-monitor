from litestar import Litestar
from litestar.di import Provide
from .api import routes
from .eom.client import Client
from .device.device import Device
from .services.device_service import DeviceService
import logging
import asyncio
import os
from contextlib import asynccontextmanager

# Set this when debugging. Save me from stupid software
logging.basicConfig(level=logging.DEBUG)
# logging.basicConfig(level=logging.INFO)

eom_ip = os.environ["EOM_IP"]
eom_port = int(os.environ["EOM_PORT"])

client = Client(ip=eom_ip, port=eom_port)
device = Device()
service = DeviceService(client, device)

@asynccontextmanager
async def lifespan(app: Litestar):

    print("Starting application")
    if not client.port_probe():
        raise RuntimeError("Device unavailable")
    
    # Yes, really; start these tasks and proceed
    client_task = asyncio.create_task(client.run())
    service_task = asyncio.create_task(service.run())

    # Wait for shutdown to commence
    yield

    # Run shutdown tasks
    print("Stopping application")
    await service.close()

    client_task.cancel()
    service_task.cancel()

    await asyncio.gather(
        client_task,
        service_task,
        return_exceptions=True,
    )

# async def startup():
#     # Connect and start up
#     logging.debug("*** LITESTAR - DEBUG START CONFIRMED ***")

#     tasks = [
#         asyncio.create_task(client.run()),
#         asyncio.create_task(service.run()),
#     ]

#     await asyncio.gather(*tasks)

# # Close the connection on shutdown
# async def shutdown() -> None:
#     await service.close()

# Litestar app configuration
app = Litestar(
    route_handlers=[
        routes.get_config, 
        routes.get_readings,
        routes.get_readings_history,
        routes.restart_device,
        routes.start_stream,
        routes.get_info,
        # set_mode, 
        # set_motor_speed,
        # set_config
    ],
    lifespan=[lifespan],
    dependencies={
        "service": Provide(lambda: service),
    }
    # on_shutdown=[shutdown],
    # on_startup=[startup]
)