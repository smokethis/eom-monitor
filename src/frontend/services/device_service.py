import asyncio
from shared.device.device import Device
from ..api.client import LitestarApiClient

class DeviceService:
    def __init__(self, client: LitestarApiClient, device: Device):
        self.device = device
        self.client = client
    
    async def start(self):
        await self.initialise()

        # self.task = asyncio.create_task(
        #     self.listen()
        # )
    
    async def initialise(self):
        config = await self.client.get_config()
        info = await self.client.get_info()
        self.update_from_config(config)
        self.update_from_info(info)

    def update_from_config(self, config):
        self.device.update_from_config(config)
    
    def update_from_info(self, info):
        self.device.update_from_info(info)

        
    
    # async def listen(self):
    #     async for event in self.client.events():
    #         self.handle_event(event)


    def apply_update(self, update):
        target = self.device

        parts = update.path.split(".")

        for part in parts[:-1]:
            target = getattr(target, part)

        setattr(target, parts[-1], update.value)