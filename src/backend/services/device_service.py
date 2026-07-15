import asyncio
from ..eom.websocketclient import Client, ClientState
from .device_bus import DeviceEventBus
from ...shared.models.messages import InfoMessage, ConfigMessage, ReadingsMessage, WifiStatusMessage
from ...shared.device.device import Device, DeviceRaw
import logging
from enum import Enum
from dataclasses import fields
from copy import deepcopy

# Get a logger specific to this file
logger = logging.getLogger(__name__)

class DeviceState(Enum):
    STANDBY = "STANDBY"
    STREAMING = "STREAMING"

class DeviceService():
    def __init__(self, client: Client, device: Device, raw: DeviceRaw, event_bus: DeviceEventBus):
        self.client = client
        self.device = device
        self.raw = raw
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
        self.raw.configuration = message
    
    def _apply_info(self, message: InfoMessage):
        self.device.update_from_info(message)
        self.raw.info = message
    
    def _apply_readings(self, message: ReadingsMessage):
        self.device.update_from_readings(message)
        self.raw.readings = message
        self.raw.readings_history.append(message)

    def _apply_wifistatus(self, message: WifiStatusMessage):
        # self.device.update_from_wifistatus(message)
        pass

    def _process_message(self, message):
        match message:
            case ConfigMessage():
                old = deepcopy(self.get_device()) # We use deepcopy() to get a copy of Device() as opposed to just a reference to the current object, it needs to be deepcopy() to cater to nested objects
                self._apply_config(message)
                new = self.get_device()
                changes = self.diff_device(old, new)
                self.publish_to_bus(changes)
            case InfoMessage():
                old = deepcopy(self.get_device())
                self._apply_info(message)
                new = self.get_device()
                changes = self.diff_device(old, new)
                self.publish_to_bus(changes)
            case ReadingsMessage():
                old = deepcopy(self.get_device())
                self._apply_readings(message)
                new = self.get_device()
                changes = self.diff_device(old, new)
                self.publish_to_bus(changes)
            case WifiStatusMessage():
                old = deepcopy(self.get_device())
                self._apply_wifistatus(message)
                new = self.get_device()
                changes = self.diff_device(old, new)
                self.publish_to_bus(changes)
            case _:
                logger.warning("Unknown message recevied: %t", type(message))
    
    def publish_to_bus(self, changes):
        self.event_bus.publish(changes)
    
    def get_device(self) -> Device:
        return self.device

    def diff_device(self, old, new):
        changes = {}

        for field in fields(new):
            old_value = getattr(old, field.name)
            new_value = getattr(new, field.name)

            if old_value != new_value:
                changes[field.name] = new_value

        return changes

    async def _listen(self):
        while True:
            logger.debug("Listening for messages on internal queue...")
            message = await self.client.events.get()
            logger.debug(f"Got message: {message!r}")
            self._process_message(message)
            logger.debug("Processed message")

    async def run(self):
        while True:
            await self._listen()