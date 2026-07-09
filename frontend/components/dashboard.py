import json
from nicegui import ui
from components.config_card import ConfigCard

class Dashboard:
    def __init__(self, client, stream):
        self.client = client
        self.stream = stream
        self.alive = True
        self.latest_event = None

    async def render(self):

        ui.label("Dashboard").classes("text-3xl")

        config = await self.client.get_config()

        with ui.row():
            ui.button(
                "Start stream",
                on_click=self.start_events
            )
            ui.button(
                "Restart device",
                on_click=self.restart_device
            )

        with ui.row():
            ConfigCard(config).render()
            self.latest_event = ui.code("Waiting for events...",language="json")

        self.stream.subscribe(self.handle_event)

        await self.stream.start()

    async def start_events(self):

        ui.notify("Starting event stream...")
        await self.client.start_readings()

    async def restart_device(self):

        ui.notify("Restarting device...")
        await self.client.restart()

    async def handle_event(self, event):

        if not self.alive:
            return

        self.latest_event.content = json.dumps(event, indent=2) # type: ignore
        self.latest_event.update() # type: ignore

    def cleanup(self):

        self.alive = False
        self.stream.unsubscribe(self.handle_event)