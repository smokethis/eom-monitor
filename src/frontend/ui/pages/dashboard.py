from nicegui import ui
from src.frontend.api.client import LitestarApiClient
from src.frontend.services.device_service import DeviceService

class Dashboard:
    def __init__(self, client: LitestarApiClient, service: DeviceService):
        self.client = client
        self.service = service

    def render(self):
        ui.label("Dashboard").classes("text-3xl")

        with ui.row():
            ui.button("Initialise", on_click=self.initialise_and_refresh)
            ui.button("Start stream", on_click=self.client.start_stream)
            ui.button("Restart device", on_click=self.client.restart)

        with ui.row():
            self.info_card()

    def info_card(self):
        with ui.card():
            ui.label(f"Hostname: {self.service.device.name}")
            ui.label(f"Arousal Threshold: {self.service.device.edging_controls.arousal_threshold}")
            ui.label(f"Sensor Sensitivity: {self.service.device.edging_controls.sensor_sensitivity}")

    async def initialise_and_refresh(self):
        await self.service.initialise()
        ui.navigate.reload()

    def restart_device(self):
        # This is fucked and I don't know why. It never runs.
        ui.notify("Restarting device...")
