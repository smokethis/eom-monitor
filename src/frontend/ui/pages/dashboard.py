from nicegui import ui
from src.frontend.api.client import LitestarApiClient
from src.frontend.services.device_service import DeviceService
from src.frontend.ui.components.layout import page_layout

class Dashboard:
    def __init__(self, client: LitestarApiClient, service: DeviceService):
        self.client = client
        self.service = service

    def render(self):
        with page_layout("EOM Dashboard"):

            backend_icon = ui.icon("s_error").classes("text-2xl")
            serial_icon = ui.icon("s_error").classes("text-2xl")
            websocket_icon = ui.icon("s_error").classes("text-2xl")

            with ui.card():
                with ui.row():
                    ui.label("Backend connected:")
                    # backend_icon.bind_name_from(self.service, "connection_icon")
                with ui.row():
                    ui.label("Device serial connected:")
                    StatusIcon(self.service, "serial")
                with ui.row():
                    ui.label("Device websocket connected:")
                    StatusIcon(self.service, "websocket")
            with ui.row():
                ui.button("Initialise", on_click=self.initialise_and_refresh)
                ui.button("Refresh Device", on_click=self.refresh_device)
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
    
    async def refresh_device(self):
        await self.service.refresh_device()
        ui.navigate.reload()

    def restart_device(self):
        # This is fucked and I don't know why. It never runs.
        ui.notify("Restarting device...")

class StatusIcon(ui.icon):
    def __init__(self, service: DeviceService, connection: str):
        self.service = service
        super().__init__("s_help")
        self.classes("text-2xl")

        self.bind_name_from(service, f"{connection}_connection_icon")

        # service.subscribe(self.update_status)
        # self.update_status(connection)

    # def update_status(self, connection):
    #     col = "color={self.service." + connection + "_connection_color}"
    #     self.props(col)