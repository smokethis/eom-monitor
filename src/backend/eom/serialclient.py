import asyncio
import serial_asyncio
import csv
from src.shared.models.messages import SerialMessage

class SerialClient:
    def __init__(self, port, baud):
        self.port = port
        self.baud = baud
        self.events = asyncio.Queue()

    async def run(self) -> str:
        while True:
            try:
                reader, writer = await serial_asyncio.open_serial_connection(
                    url=self.port,
                    baudrate=self.baud,
                )

                while True:
                    line = await reader.readline()

                    if not line:
                        break

                    r = self.parse_line(line.decode().strip())
                    await self.events.put(r)

            except Exception as ex:
                print(ex)
                await asyncio.sleep(2)

    def handle_line(self, line:str):
        print(line)

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