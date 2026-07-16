import asyncio
import serial_asyncio_fast
import csv
from src.shared.models.messages import SerialMessage
from src.shared.models.modes import ConnectionState
import logging

# Get a logger specific to this file
logger = logging.getLogger(__name__)
# Debug mode on
logging.basicConfig(level=logging.DEBUG)

class SerialClient:
    def __init__(self, port, baud):
        self.port = port
        self.baud = baud
        self.messages = asyncio.Queue(1000)
        self.connection_status = asyncio.Queue(5)

    async def run(self) -> str:

        logger.debug("Attempting to open serial: %s", self.port)
        while True:
            try:
                reader, writer = await serial_asyncio_fast.open_serial_connection(
                    url=self.port,
                    baudrate=self.baud,
                )
                await self.connection_status.put(ConnectionState.Connected)
                logger.debug("Serial connection opened")

                while True:
                    line = await reader.readline()

                    if not line:
                        break

                    m = self.parse_line(line.decode().strip())
                    await self.messages.put(m)
            
            except asyncio.CancelledError:
                logger.info("Serial client stopping")
                raise

            except Exception as ex:
                await self.connection_status.put(ConnectionState.Error)
                print(ex)

            await asyncio.sleep(2)

    def parse_line(self, line: str) -> SerialMessage | None:

        EXPECTED_FIELDS = 10

        # Ignore diagnostics
        if line.startswith("MEM:"):
            return None

        try:
            row = next(csv.reader([line]))
        except csv.Error:
            return None

        if len(row) != EXPECTED_FIELDS:
            return None

        return SerialMessage(
            pavg=int(row[0]),
            arousal=int(row[1]),
            motor=int(row[2]),
            sensitivity_threshold=int(row[3]),
            detect_state=int(row[4]),
            detect_rhytmic=row[5],
            detect_baseline=int(row[6]),
            detect_sustained_ms=int(row[7]),
            detect_peak_count=int(row[8]),
            detect_last_interval_ms=int(row[9])
        )