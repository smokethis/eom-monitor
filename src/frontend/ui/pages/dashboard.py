from nicegui import ui
from src.frontend.api.client import LitestarApiClient
from src.frontend.ui.widgets.info_card import InfoCard
from src.frontend.services.device_service import DeviceService
from src.frontend.ui.viewmodels.readings_vm import ReadingsViewModel

class Dashboard:
    def __init__(self, client: LitestarApiClient, service: DeviceService):
        self.client = client
        self.service = service

    async def render(self):

        ui.label("Dashboard").classes("text-3xl")
        vm = ReadingsViewModel(self.service)

        with ui.row():
            ui.button("Initialise", on_click=self.initialise_and_refresh)
            ui.button("Start stream", on_click=self.client.start_stream)
            ui.button("Restart device", on_click=self.client.restart)

        with ui.row():
            InfoCard(self.service).render()
            # self.latest_event = ui.code("Waiting for events...",language="json")

        with ui.row():
            ui.label().bind_text_from(vm, 'arousal_level')
            ui.label().bind_text_from(vm, 'pressure')
            ui.label().bind_text_from(vm, 'time_since_power_on')

    async def initialise_and_refresh(self):
        await self.service.initialise()
        ui.navigate.reload()

    async def restart_device(self):

        ui.notify("Restarting device...")
        # await self.client.restart()

    # async def handle_event(self, event):

    #     if not self.alive:
    #         return

    #     self.latest_event.content = json.dumps(event, indent=2) # type: ignore
    #     self.latest_event.update() # type: ignore

    # def cleanup(self):

    #     self.alive = False
    #     # self.stream.unsubscribe(self.handle_event)