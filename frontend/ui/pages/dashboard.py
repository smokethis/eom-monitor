import json
from nicegui import ui
from frontend.ui.widgets.info_card import InfoCard

class Dashboard:
    def __init__(self, device):
        self.device = device
        self.alive = True

    async def render(self):

        ui.label("Dashboard").classes("text-3xl")

        with ui.row():
            ui.button(
                "Start stream",
                # on_click=self.start_stream
            )
            ui.button(
                "Restart device",
                # on_click=self.restart_device
            )

        with ui.row():
            InfoCard(self.device).render()
            # self.latest_event = ui.code("Waiting for events...",language="json")

        # self.stream.subscribe(self.handle_event)

        # await self.stream.start()

    # async def start_stream(self):

    #     ui.notify("Starting event stream...")
    #     await self.client.start_stream()

    async def restart_device(self):

        ui.notify("Restarting device...")
        # await self.client.restart()

    async def handle_event(self, event):

        if not self.alive:
            return

        self.latest_event.content = json.dumps(event, indent=2) # type: ignore
        self.latest_event.update() # type: ignore

    def cleanup(self):

        self.alive = False
        # self.stream.unsubscribe(self.handle_event)