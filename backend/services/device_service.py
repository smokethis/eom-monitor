import asyncio
from ..eom.client import Client, ClientState
from ..services.device_bus import DeviceEventBus
from ..eom.models import InfoMessage, ConfigMessage, ReadingsMessage, WifiStatusMessage
from ..device.device import Device
import logging
from enum import Enum
import msgspec

# Get a logger specific to this file
logger = logging.getLogger(__name__)

class DeviceState(Enum):
    STANDBY = "STANDBY"
    STREAMING = "STREAMING"

class DeviceService():
    def __init__(self, client: Client, device: Device, event_bus: DeviceEventBus):
        self.client = client
        self.device = device
        self.state = DeviceState.STANDBY
        self.event_bus = event_bus

    async def restart(self) -> bool:
        await self.client.send_restart_command()
        # Yield to asyncio for a bit to try and empty any ready tasks including restart to mitigate early false positives in the port probe loop
        await asyncio.sleep(0)
        await asyncio.sleep(1)
        # Start probing for port 80
        logger.info("Starting port probe loop...")
        r = self.client.wait_until_available(timeout=10) # This is deliberately blocking to ensure we do nothing else until a response or timeout
        # Return result to caller
        if r != False:
            logger.info("Port 80 re-opened. Exiting.")
            # The server looks alive again, confirm
            return True
        else:
            logger.error("Webserver never recovered. Check device.")
            # The server appears dead, fail
            return False
    
    async def close(self) -> None:
        if self.client.state is ClientState.CONNECTED:
            """ We can't close the connection gracefully right now, ws.close() doesn't work and
             there is a socket leak in the EOM v2.0.0 firmware; no matter what you do you will reach
             the 3 socket maximum at some point and the HTTP server will stop new connections. 
             Instead we reset the device and then force Litestar to terminate the transport to ensure 
             a clean break from both sides. This doesn't work once a stream has started though. So 
             good luck figuring that out. Best idea is to force Litestar/Uvicron to end, reconnect and
             manually trigger a restart to restore order. Sigh."""
            logger.info("Request to close received...")
            await self.restart()
            self.client.close_connection()

    async def start_readings(self) -> None:
        await self.client.send_start_readings_command()
        self.state = DeviceState.STREAMING

    def _apply_config(self, message: ConfigMessage):
        self.device.update_from_config(message)
        self.device.config = message
        self.publish_to_bus(message)
    
    def _apply_info(self, message: InfoMessage):
        self.device.update_from_info(message)
        self.device.info = message
        self.publish_to_bus(message)
    
    def _apply_readings(self, message: ReadingsMessage):
        self.device.update_from_readings(message)
        self.device.raw_readings = message
        self.publish_to_bus(message)

    def _apply_wifistatus(self, message):
        # self.device.update_from_wifistatus(message)
        pass

    def _process_message(self, message):
        match message:
            case ConfigMessage():
                self._apply_config(message)
            case InfoMessage():
                self._apply_info(message)
            case ReadingsMessage():
                self._apply_readings(message)
            case WifiStatusMessage():
                self._apply_wifistatus(message)
            case _:
                logger.warning("Unknown message recevied: %t", type(message))
    
    def publish_to_bus(self, message):
        json = msgspec.json.encode(message)
        self.event_bus.publish(json)
    
    async def get_device_state(self) -> Device:
        return self.device

    async def _listen(self):
        while True:
            message = await self.client.events.get()
            self._process_message(message)

    async def run(self):
        while True:
            await self._listen()