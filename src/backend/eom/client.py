import socket
import time
from websockets.asyncio.client import connect
import logging
import asyncio
import msgspec
from enum import Enum
from ...shared.models import models

class ClientState(Enum):
    DISCONNECTED = "DISCONNECTED"
    CONNECTED = "CONNECTED"

# Get a logger specific to this file
logger = logging.getLogger(__name__)
# Debug mode on
logging.basicConfig(level=logging.DEBUG)

class Client():
    
    def __init__(self, ip: str, port: int):
        self.uri = f"ws://{ip}:{port}/"
        self.ip = ip
        self.port = port
        self.events = asyncio.Queue() # Need to re-add maxsize, wasn't that.

    def port_probe(self):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            result = sock.connect_ex((self.ip, self.port))
            sock.close()
            return result == 0
        except:
            return False

    async def _send(self, command: str) -> None:
        if self.ws is None:
            raise RuntimeError("Websocket not connected")

        payload = {command: None}

        data = msgspec.json.encode(payload).decode("utf-8") # EOM3000 websocket handler only accepts TEXT frames. Yes we have to encode/decode. Trust.

        logger.debug("Sending text: %s", data)

        await self.ws.send(data)
    
    # async def _request(self, response_name: str, payload: dict, response_type: type):
        # async with self._request_lock:
        #     logger.debug("Requesting %s", response_name)
        #     # Create a future
        #     future = asyncio.get_running_loop().create_future()
        #     # Regsiter it
        #     self._pending[response_name] = (
        #         future,
        #         response_type,
        #     )
        #     # Send the payload
        #     logger.debug("Sending %s", payload)
        #     await self._send(payload)
        #     # Start a timer to wait for a response
        #     try:
        #         logger.debug("Waiting for %s", response_name)
        #         return await asyncio.wait_for(
        #             future,
        #             timeout=10,
        #         )

        #     finally:
        #         self._pending.pop(response_name, None)

    def wait_until_available(self, timeout=30) -> bool:
        deadline = time.monotonic() + timeout

        while time.monotonic() < deadline:
            if self.port_probe():
                return True

            time.sleep(1)

        return False

    async def send_restart_command(self) -> None:
        logger.debug("Sending restart command...")
        await self._send("restart")

    async def send_start_readings_command(self) -> None:
        logger.debug("Sending stream start command...")
        await self._send("streamReadings")
    
    async def request_config(self) -> None:
        logger.debug("Sending config request command...")
        await self._send("configList")
    
    async def request_info(self) -> None:
        logger.debug("Sending info request command...")
        await self._send("info")

    def close_connection(self) -> None:
            self.ws.transport.close()

    def decode_message(self, raw):
        logger.debug("RX raw: %r", raw)

        if isinstance(raw, str):
            msg = raw.encode()

        msg = msgspec.json.decode(raw, type=object)

        for key, value in msg.items(): # type: ignore

            # Readings path
            if key == "readings":
                reading = msgspec.convert(value, type=models.ReadingsMessage)
                return reading

            # wifiStatus path
            if key == "wifiStatus":
                wifi_status = msgspec.convert(value, type=models.WifiStatusMessage)
                return wifi_status

            # Config path
            if key == "configList":
                config = msgspec.convert(value, type=models.ConfigMessage)
                return config
            
            # Info path
            if key == "info":
                info = msgspec.convert(value, type=models.InfoMessage)
                return info
                        
            # SDcard path not implemented yet
            
            #Whinge about unexpected message types
            logger.debug("Ignoring message type %s", key)

    # async def _writer(self):
    #     while True:
    #         command = await self.commands.get()
    #         await self.ws.send(command)

    async def _handle_message(self, raw):
        message = self.decode_message(raw)
        logger.debug("Decoded message: %s", type(message))
        if message: 
            await self.events.put(message)

    async def _reader(self):
        async for message in self.ws:
            logger.debug("Recevied frame: %r", message)
            await self._handle_message(message)

    async def run(self):
        while True:
            try:
                async with connect(self.uri, ping_interval=None) as ws: # Disabled ping as the device is a nonsense
                    self.ws = ws
                    self.state = ClientState.CONNECTED
                    logger.info("Connected to device")

                    reader_task = asyncio.create_task(self._reader())

                    await self.request_config()
                    await self.request_info()

                    await reader_task

            except asyncio.CancelledError:
                logger.info("Websocket client stopping")
                raise

            except Exception as e:
                logger.warning("Connection error: %s", e)
                self.state = ClientState.DISCONNECTED
                logger.warning("Retrying in 5 seconds...")
                await asyncio.sleep(5)
        
    # async def run(self):
    #     try:
    #         async with connect(self.uri, ping_interval=None) as ws: # Disabled ping for debugging
    #             self.ws = ws

    #             logger.info("Connected")

    #             self.state = ClientState.CONNECTED

    #             reader = asyncio.create_task(self._reader())
                
    #             await asyncio.gather(
    #                 reader,
    #                 # self._writer(),
    #             )

        