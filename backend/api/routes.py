from litestar import get, post, WebSocket
from litestar.exceptions import HTTPException
from ..eom.models import InfoMessage, ConfigMessage, ReadingsMessage, WifiStatusMessage
from ..device.device import Device
from ..services.device_bus import DeviceEventBus
from collections import deque
import msgspec
from ..services.device_service import DeviceService
import asyncio

json_encoder = msgspec.json.Encoder()

# Readings API Endpoint.
# @get("/api/readings")
# async def get_readings() -> ServerSentEvent:

#     queue = eom.readings_bus.subscribe()
#     logging.debug("Subscriber Joined Queue")

#     async def stream():
#         try:
#             while True:
#                 reading = await queue.get()
#                 yield {
#                     "event": "message",
#                     "data": json_encoder.encode(reading).decode()
#                     }

#         finally:
#             eom.readings_bus.unsubscribe(queue)
#             logging.debug("Subscriber Left Queue")

#     return ServerSentEvent(stream())

# Static API Endpoints
@get("/api/raw/config")
async def get_config(service: DeviceService) -> ConfigMessage:
    if service.device.config is None:
        raise HTTPException(
            status_code=503,
            detail="Device configuration is not available yet",
        )
    return service.device.config

@get("/api/raw/info")
async def get_info(service: DeviceService) -> InfoMessage:
    if service.device.info is None:
        raise HTTPException(
            status_code=503,
            detail="Device info is not available yet",
        )
    return service.device.info

@post("/api/raw/start_stream")
async def start_stream(service: DeviceService) -> None:
    await service.start_readings()

# @post("/config")
# async def set_config(
#     data: EdgeOMaticConfig
# ) -> Dict[str, str]:
#     """Update the EdgeOMatic configuration."""
#     eom.set_config(data)
#     return {"status": "success"}

@get("/api/raw/readings")
async def get_readings(service: DeviceService) -> ReadingsMessage:
    if not service.state == "STREAMING":
        raise HTTPException(
            status_code=409,
            detail="Streaming has not been started. Call POST /api/start_stream first."
        )
    return service.device.raw_readings

@get("/api/raw/readings/history")
async def get_readings_history(service: DeviceService) -> deque:
    if not service.state == "STREAMING":
        raise HTTPException(
            status_code=409,
            detail="Streaming has not been started. Call POST /api/start_stream first."
        )
    return service.device.raw_readings_history

@get("/api/device")
async def get_device(service: DeviceService) -> Device:
    return service.device

@get("/api/service")
async def get_service(service: DeviceService) -> DeviceService:
    return service

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
async def restart_device(service: DeviceService) -> None:
    await service.restart()

@get("/ws/devices")
async def device_socket(socket: WebSocket, bus: DeviceEventBus):
    await socket.accept()

    queue = bus.subscribe()

    try:
        while True:
            device = await queue.get()

            await socket.send_json({
                "id": device.id,
                "temperature": device.temperature,
                "status": device.status,
            })

    finally:
        bus.unsubscribe(queue)