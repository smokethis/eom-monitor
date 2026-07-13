import asyncio
import json
import httpx

from src.frontend.api.client import LITESTAR_BASE

class EventStream:

    def __init__(self):
        self.listeners = set()
        self.task = None
        self.running = False

    def subscribe(self, callback):
        self.listeners.add(callback)

    def unsubscribe(self, callback):
        self.listeners.discard(callback)

    async def start(self):
        if self.task:
            return

        self.running = True
        self.task = asyncio.create_task(self._run())

    async def stop(self):
        self.running = False

        if self.task:
            self.task.cancel()
            self.task = None

    async def _run(self):

        async with httpx.AsyncClient(timeout=None) as client:

            async with client.stream(
                "GET",
                f"{LITESTAR_BASE}/api/readings"
            ) as response:

                async for line in response.aiter_lines():

                    if not self.running:
                        break

                    if line.startswith("data:"):

                        payload = line[5:].strip()

                        if payload:
                            event = json.loads(payload)

                            for listener in list(self.listeners):
                                await listener(event)