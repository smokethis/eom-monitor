import msgspec
from websockets.asyncio.client import connect
from msgspec import Struct
from enum import Enum
import logging
import asyncio
from collections import deque
from typing import Literal
from enum import Enum

# Get a logger specific to this file
logger = logging.getLogger(__name__)

class ControlMode(Enum):
    Manual = "MANUAL_CONTROL"
    Automatic = "AUTOMAITC_CONTROL"
    Orgasm = "ORGASM_MODE"
    Unk = ""

class VibrationMode(Enum):
    GlobalSync = 0
    RampStop = 1
    Depletion = 2
    Enhancement = 3

class EdgeOMaticConfig(Struct):
    wifi_ssid: str
    wifi_key: str
    wifi_on: bool
    bt_display_name: str
    bt_on: bool
    force_bt_coex: bool
    led_brightness: int
    websocket_port: int
    use_ssl: bool
    hostname: str
    motor_min_speed: int
    motor_max_speed: int
    motor_ramp_time_s: int
    cooldown_delay_ms: int
    cooldown_random_ms: int
    arousal_holdoff_ms: int
    screen_dim_seconds: int
    screen_timeout_seconds: int
    reverse_menu_scroll: bool
    pressure_smoothing: int
    classic_serial: bool
    sensitivity_threshold: int
    update_frequency_hz: int
    sensor_sensitivity: int
    use_average_values: bool
    vibration_mode: VibrationMode
    # ADDED FROM v2.0 firmware config file
    _filename: str
    store_command_history: bool
    console_basic_mode: bool
    enable_screensaver: bool
    language_file_name: str
    remote_update_url: str
    version: int = msgspec.field(name="$version")
    mdns_enabled: bool
    denial_count_mode: int
    arousal_decay_rate: int
    od_mode: int
    od_sustained_threshold: int
    od_sustained_fallback_ms: int
    od_sustained_dropout_ms: int
    od_peak_min_amplitude: int
    od_rhythmic_min_peaks: int
    od_rhythmic_interval_min_ms: int
    od_rhythmic_interval_max_ms: int
    od_rhythmic_interval_variance_ms: int
    od_rhythmic_timeout_ms: int
    od_arousal_gate_percent: int
    od_recovery_ms: int
    od_clench_arousal_boost: bool
    od_clench_arousal_boost_amount: int
    od_detection_armed: bool

class EdgeOMaticReadings(Struct):
    pressure: int
    pavg: int
    motor: int
    arousal: int
    millis: int
    run_mode: ControlMode = msgspec.field(name="runMode")

    # REMOVED IN firmware v2.0 broadcast.c
    # permit_orgasm: bool = msgspec.field(name="permitOrgasm")
    # post_orgasm: bool = msgspec.field(name="postOrgasm")
    # lock: bool

    # NEW FIELDS FROM firmware v2.0 broadcast.c:
    detect_state: str = msgspec.field(name="detectState")
    detect_baseline: int = msgspec.field(name="detectBaseline")
    detect_peak_count: int = msgspec.field(name="detectPeakCount")
    detect_sustained_ms: int = msgspec.field(name="detectSustainedMs")
    detect_last_interval_ms: int = msgspec.field(name="detectLastIntervalMs")

class EdgeOMaticInfo(Struct):
    device: str
    serial: str
    hw_version: str = msgspec.field(name="hwVersion")
    fw_version: str = msgspec.field(name="fwVersion")

class EdgeOMaticWifiStatus(Struct): # Defaults because there may not be any information immediately
    ssid: str = ""
    ip: str = ""
    rssi: int = -1

class EdgeOMaticReadingsBus:
    def __init__(self, queue_size: int = 1):
        self._queue_size = queue_size
        self._subscribers: set[asyncio.Queue] = set()

    def subscribe(self) -> asyncio.Queue:
        queue = asyncio.Queue(maxsize=self._queue_size)
        self._subscribers.add(queue)
        return queue

    def unsubscribe(self, queue: asyncio.Queue):
        self._subscribers.discard(queue)

    async def publish(self, reading):
        for queue in list(self._subscribers):
            if queue.full():
                try:
                    queue.get_nowait()
                except asyncio.QueueEmpty:
                    pass

            await queue.put(reading)

class EdgeOMaticStatus(Enum):
    DISCONNECTED = "DISCONNECTED"
    CONFIGURING = "CONFIGURING"
    READY = "READY"
    STREAMING = "STREAMING"

class EdgeOMatic: # Main object that runs the show
    def __init__(self, ip: str, port: int):
        self.uri = f"ws://{ip}:{port}/"
        self.readings = None
        self._config = None
        self._info = None
        self._pending: dict[str, tuple[asyncio.Future, type]] = {}
        self._request_lock = asyncio.Lock()
        self.latest_reading = None
        self.reading_history = deque(maxlen=100)
        self.readings_bus = EdgeOMaticReadingsBus()
        self.state = EdgeOMaticStatus.DISCONNECTED
    
    @property
    def config(self):
        return self._config
    
    @property
    def info(self):
        return self._info

    async def _send(self, payload: dict):
        if self.ws is None:
            raise RuntimeError("Websocket not connected")

        # EOM3000 websocket handler only accepts TEXT frames. Yes we have to encode/decode. Trust.
        data = msgspec.json.encode(payload).decode("utf-8")

        logger.debug("Sending text: %s", data)

        await self.ws.send(data)
    
    async def _request(self, response_name: str, payload: dict, response_type: type):
        async with self._request_lock:
            logger.debug("Requesting %s", response_name)
            # Create a future
            future = asyncio.get_running_loop().create_future()
            # Regsiter it
            self._pending[response_name] = (
                future,
                response_type,
            )
            # Send the payload
            logger.debug("Sending %s", payload)
            await self._send(payload)
            # Start a timer to wait for a response
            try:
                logger.debug("Waiting for %s", response_name)
                return await asyncio.wait_for(
                    future,
                    timeout=10,
                )

            finally:
                self._pending.pop(response_name, None)

    async def _handle_message(self, message):

        logger.debug("RX raw: %r", message)

        if isinstance(message, str):
            message = message.encode()

        msg = msgspec.json.decode(message, type=object)

        for key, value in msg.items(): # type: ignore

            # Request/response path
            pending = self._pending.pop(key, None)
            if pending is not None:
                future, response_type = pending
                result = msgspec.convert(value, type=response_type)
                if not future.done():
                    future.set_result(result)
                continue

            # Event path
            if key == "readings":
                reading = msgspec.convert(value, type=EdgeOMaticReadings)
                self.latest_reading = reading
                self.reading_history.append(reading)
                await self.readings_bus.publish(reading)
                continue

            if key == "wifiStatus":
                self._wifi_status = msgspec.convert(value, type=EdgeOMaticWifiStatus)
                continue
            
            #Whinge about unexpected message types
            logger.debug("Ignoring message type %s", key)

    async def _request_config(self) -> EdgeOMaticConfig:
        return await self._request(
            "configList",
            {"configList": None},
            EdgeOMaticConfig,
        )
    
    async def _request_info(self) -> EdgeOMaticInfo:
        return await self._request(
            "info",
            {"info": None},
            EdgeOMaticInfo,
        )
    
    async def start_readings(self) -> EdgeOMaticReadings:
        return await self._request(
            "readings",
            {"streamReadings": None}, # Yes, the trigger message is different to the received schema. I hate it
            EdgeOMaticReadings,
        )
    
    async def get_readings_history(self):
        return self.reading_history

    async def restart(self) -> None:
        await self._send({
            "restart": None
        })

    async def close(self) -> None:
        if self.ws is not None:
            # logger.info("Closing connection")
            # await self.ws.close()
            # self.ws = None
            # logger.info("Connection closed")
            """ We can't close the connection gracefully right now, there's no close reply from 
            the EOM in firmware v2.0.0, and it looks like there might be a silent leak or 
            other issue somewhere as the HTTP server eventually falls over after too many app restarts.
            Insetad we'll issue a device reset command to force a clean break """
            logger.info("Request to close received, restarting device...")
            await self.restart()

    async def _reader(self):

        async for message in self.ws:
            await self._handle_message(message)

    # async def _writer(self):
    #     while True:
    #         command = await self.commands.get()
    #         await self.ws.send(command)

    async def run(self):
        while True:
            try:
                async with connect(self.uri, ping_interval=None) as ws: # Disabled ping for debugging
                    self.ws = ws

                    logger.info("Connected")

                    self.state = EdgeOMaticStatus.CONFIGURING

                    self._config = await self._request_config()
                    self._info = await self._request_info()

                    self.state = EdgeOMaticStatus.READY
                    
                    await asyncio.gather(
                        self._reader(),
                        # self._writer(),
                    )

            except Exception as e:
                logger.warning("Connection error: %s", e)
                self.state = EdgeOMaticStatus.DISCONNECTED
                logger.warning("Retrying in 5 seconds...")
                await asyncio.sleep(5)