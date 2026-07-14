from src.shared.device.device import Device
from src.frontend.api.client import LitestarApiClient

class DeviceService:
    def __init__(self, client: LitestarApiClient):
        self.device = Device()
        self.client = client
        self._listeners = []
    
    async def start(self):
        await self.initialise()
        await self.stream()

    async def initialise(self):
        info = await self.client.get_info()
        self.device.update_from_info(info)
        config = await self.client.get_config()
        self.device.update_from_config(config)
    
    def subscribe(self, callback):
        self._listeners.append(callback)

    def unsubscribe(self, callback):
        self._listeners.remove(callback)

    async def stream(self):
        await self.client.connect_stream()

        while True:
            patch = await self.client.receive_stream_message()

            self.device.apply_patch(patch)

            for callback in self._listeners:
                try:
                    callback(self.device)
                except Exception:
                    import traceback
                    traceback.print_exc()
