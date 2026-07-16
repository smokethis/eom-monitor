from nicegui import ui
from src.frontend.api.client import LitestarApiClient
from src.shared.device.device import Device
from src.frontend.services.device_service import DeviceService
from src.frontend.ui.components.layout import page_layout

class Dashboard:
    def __init__(self, client: LitestarApiClient, service: DeviceService):
        self.client = client
        self.service = service

    def render(self):
        with page_layout("EOM Dashboard"):

            with ui.card():
                with ui.row():
                    ui.label("Backend connected:")
                    ui.icon("s_check_circle", color="positive").classes("text-2xl")
                with ui.row():
                    ui.label("Device serial connected:")
                    ui.icon("s_check_circle", color="positive").classes("text-2xl")
                with ui.row():
                    ui.label("Device websocket connected:")
                    ui.icon("s_check_circle", color="positive").classes("text-2xl")
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

class StatusIcon(ui.icon):
    def check_backend_connetion(self, status: Device):
        if status.name == "ok":
            self.color = "positive"
            self.classes(replace="something in classes")
        else:
            self.color = "negative"
            self.classes(replace="something else in classes")