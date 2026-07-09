from litestar import Litestar, get, post
from litestar.template.config import TemplateConfig
from litestar.contrib.jinja import JinjaTemplateEngine
from litestar.response import Template, ServerSentEvent
from pathlib import Path
from collections import deque
from typing import Dict, Any
from eom import EdgeOMatic, EdgeOMaticConfig, EdgeOMaticReadings, EdgeOMaticInfo, EdgeOMaticReadingsBus
import logging
import asyncio

logging.basicConfig(level=logging.INFO)
eom: EdgeOMatic = EdgeOMatic("192.168.101.154", 80)

# Define Startup Logic
async def startup():
    asyncio.create_task(eom.run())

# Configure dashboard GUI routes
@get("/dashboard")
async def dashboard() -> Template:
    return Template(
        template_name="dashboard.html",
        context={
            "title": "EOM Monitor",
        },
    )

@get("/fragments/config")
async def config_panel() -> Template:
    config = await eom.get_config()

    return Template(
        "config_panel.html",
        context={
            "config": config
        }
    )

@get("/dashboard/events")
async def events() -> ServerSentEvent:

    queue = eom.readings_bus.subscribe()
    logging.debug("Subscriber Joined Queue")

    async def stream():
        try:
            while True:
                reading = await queue.get()

                yield reading

        finally:
            eom.readings_bus.unsubscribe(queue)
            logging.debug("Subscriber Left Queue")

    return ServerSentEvent(stream())

# Routes for EdgeOMatic API
@get("/api/config")
async def get_config() -> EdgeOMaticConfig:
    return await eom.get_config()

# @post("/config")
# async def set_config(
#     data: EdgeOMaticConfig
# ) -> Dict[str, str]:
#     """Update the EdgeOMatic configuration."""
#     eom.set_config(data)
#     return {"status": "success"}

@get("/api/readings")
async def get_readings() -> EdgeOMaticReadings:
    return await eom.get_readings()

@get("/api/readings/history")
async def get_readings_history() -> deque:
    return await eom.get_readings_history()

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

@get("/api/info")
async def get_info() -> EdgeOMaticInfo:
    """Get information about the EdgeOMatic device."""
    return await eom.get_info()

# Create a lifecycle hook to close the connection when the app shuts down
# def on_shutdown() -> None:
#     global eom
#     if eom is not None:
#         try:
#             eom.restart()
#         except Exception as e:
#             logging.error(f"Error during shutdown: {e}")

# Litestar app configuration
app = Litestar(
    route_handlers=[
        get_config, 
        # set_config, 
        get_readings,
        get_readings_history,
        # set_mode, 
        # set_motor_speed, 
        restart_device, 
        get_info,
        dashboard,
        config_panel,
        events
    ],
    # on_shutdown=[on_shutdown],
    on_startup=[startup],
    template_config=TemplateConfig(
        directory=Path("templates"),
        engine=JinjaTemplateEngine,
    ),
)