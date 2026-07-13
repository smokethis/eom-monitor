from shared.device.device import Device
from frontend.api.client import LitestarApiClient

class DeviceService:
    def __init__(self, client: LitestarApiClient):
        self.device = Device()
        self.client = client
    
    async def start(self):
        await self.initialise()

        # self.task = asyncio.create_task(
        #     self.listen()
        # )
    
    async def initialise(self):
        info = await self.client.get_info()
        self.device.update_from_info(info)
        config = await self.client.get_config()
        self.device.update_from_config(config)
        
    
    # async def listen(self):
    #     async for event in self.client.events():
    #         self.handle_event(event)


    # def apply_update(self, update):
    #     target = self.device

    #     parts = update.path.split(".")

    #     for part in parts[:-1]:
    #         target = getattr(target, part)

    #     setattr(target, parts[-1], update.value)