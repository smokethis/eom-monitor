from litestar import Litestar, get, post
from litestar.response import ServerSentEvent
from collections import deque
from typing import Dict, Any
from eom import EdgeOMatic
import logging
import asyncio
import msgspec
import os

json_encoder = msgspec.json.Encoder()
eom_ip = os.environ["EOM_IP"]
eom_port = int(os.environ["EOM_PORT"])

logging.basicConfig(level=logging.INFO)
eom: EdgeOMatic = EdgeOMatic(eom_ip, eom_port)

# Define Startup Logic
async def startup():
    # Connect and start up
    asyncio.create_task(eom.run()) ### Needs a way to handle connection failures but I can't be arsed right now

# Events API Endpoint.
@get("/api/events")
async def events() -> ServerSentEvent:

    queue = eom.readings_bus.subscribe()
    logging.debug("Subscriber Joined Queue")

    async def stream():
        try:
            while True:
                reading = await queue.get()
                yield {
                    "event": "message",
                    "data": json_encoder.encode(reading).decode()
                    }

        finally:
            eom.readings_bus.unsubscribe(queue)
            logging.debug("Subscriber Left Queue")

    return ServerSentEvent(stream())

# Static API Endpoints
@get("/api/config")
async def config() -> Any:
    return eom.config

@get("/api/info")
async def info() -> Any:
    return eom.info

@post("/api/start_stream")
async def start_stream() -> None:
    await eom.start_readings()

# @post("/config")
# async def set_config(
#     data: EdgeOMaticConfig
# ) -> Dict[str, str]:
#     """Update the EdgeOMatic configuration."""
#     eom.set_config(data)
#     return {"status": "success"}

@get("/api/reading")
async def get_reading() -> Any:
    return await eom.get_reading()

@get("/api/reading/history")
async def get_reading_history() -> deque:
    return await eom.get_reading_history()

# @post("/mode/{mode:str}")
# async def set_mode(
#     mode: str
# ) -> Dict[str, Any]:
#     """Set the EdgeOMatic control mode."""
#     try:
#         control_mode = ControlMode(mode)
#         result = eom.set_mode(control_mode)
#         return {"status": "success", "result": result}
#     except ValueError:
#         return {"status": "error", "message": f"Invalid mode: {mode}"}

# @post("/motor/{speed:int}")
# async def set_motor_speed(
#     speed: int
# ) -> Dict[str, Any]:
#     """Set the EdgeOMatic motor speed."""
#     result = eom.set_motor_speed(speed)
#     return {"status": "success", "result": result}

@post("/api/restart")
async def restart_device() -> Dict[str, Any]:
    result = await eom.restart()
    return {"status": "success", "result": result}

# Close the connection on shutdown
async def shutdown() -> None:
    await eom.close()

# Litestar app configuration
app = Litestar(
    route_handlers=[
        config, 
        get_reading,
        get_reading_history,
        restart_device,
        start_stream,
        info,
        events,
        # set_mode, 
        # set_motor_speed,
        # set_config
    ],
    on_shutdown=[shutdown],
    on_startup=[startup]
)