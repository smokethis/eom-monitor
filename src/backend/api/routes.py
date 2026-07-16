from litestar import get, post, WebSocket, websocket
from litestar.exceptions import HTTPException
from ...shared.models.messages import InfoMessage, ConfigMessage, ReadingsMessage, WifiStatusMessage
from ...shared.device.device import Device
from ..services.device_bus import DeviceEventBus
from collections import deque
import msgspec
from ..services.device_service import DeviceService, StreamState

clients: set[WebSocket] = set()

json_encoder = msgspec.json.Encoder()

# Static API Endpoints
@get("/api/raw/config")
async def get_config(service: DeviceService) -> ConfigMessage:
    if service.raw.configuration is None:
        raise HTTPException(
            status_code=503,
            detail="Device configuration has not been received",
        )
    return service.raw.configuration

@get("/api/raw/info")
async def get_info(service: DeviceService) -> InfoMessage:
    if service.raw.info is None:
        raise HTTPException(
            status_code=503,
            detail="Device info has not been received",
        )
    return service.raw.info

@post("/api/update/info")
async def update_info(service: DeviceService) -> None:
    await service.client.request_info()

@post("/api/update/config")
async def update_config(service: DeviceService) -> None:
    await service.client.request_config()

@post("/api/start_stream")
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
    if not service.stream_state == StreamState.STREAMING:
        raise HTTPException(
            status_code=409,
            detail="Streaming has not been started. Call POST /api/start_stream first."
        )
    return service.raw.readings

@get("/api/raw/readings/history")
async def get_readings_history(service: DeviceService) -> deque:
    if not service.stream_state == StreamState.STREAMING:
        raise HTTPException(
            status_code=409,
            detail="Streaming has not been started. Call POST /api/start_stream first."
        )
    return service.raw.readings_history

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

# @websocket("/api/stream")
# async def stream(socket: WebSocket, bus: DeviceEventBus) -> None:
#     print("🚀 websocket handler entered")

#     await socket.accept()

#     queue = bus.subscribe()

#     while True:
#         event = await queue.get()
#         await socket.send_json(event)

@websocket("/api/stream")
async def stream(socket: WebSocket, event_bus: DeviceEventBus) -> None:
    await socket.accept()

    queue = event_bus.subscribe()

    try:
        while True:
            event = await queue.get()
            await socket.send_json(event)

    finally:
        event_bus.unsubscribe(queue)
