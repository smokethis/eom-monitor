from nicegui import ui
from src.frontend.api.client import LitestarApiClient
from src.frontend.services.device_service import DeviceService
from src.shared.models.modes import ConnectionState
from src.frontend.ui.components.header import PageHeader

class Dashboard:
    def __init__(self, client: LitestarApiClient, service: DeviceService):
        self.client = client
        self.service = service

    def render(self):

        PageHeader("EOM Dashboard")

        with ui.row():
            ui.button("Initialise", on_click=self.initialise_and_refresh)
            ui.button("Refresh Device", on_click=self.refresh_device)
            ui.button("Start stream", on_click=self.client.start_stream)
            ui.button("Restart device", on_click=self.client.restart)
        with ui.card():
            with ui.column():
                with ui.row():
                    ui.label("Connection Status:")
                with ui.row():
                    # backend_icon.bind_name_from(self.service, "connection_icon")
                    StatusBadge(self.service, "serial")
                    StatusBadge(self.service, "websocket")

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

class StatusBadge(ui.badge):
    def __init__(self, service: DeviceService, connection: str):
        super().__init__(text=connection)
        self.service = service
        self.connection = connection
        self.props('rounded')
        self.classes('q-mr-sm')
        
        # Set initial color
        self._sync_color()
        
        # Poll for status changes (every 2 seconds)
        ui.timer(2.0, self._sync_color)

    def _sync_color(self):
        # Replace with your actual status check logic
        match self.connection:
            case "serial":
                conn = self.service.device.state.serial_connection
            case "websocket":
                conn = self.service.device.state.websocket_connection
        match conn:
            case ConnectionState.Connected:
                color = 'positive'
            case ConnectionState.Disconnected:
                color = 'negative'
            case _:
                color = 'grey'
        self.props(f'color={color}')
