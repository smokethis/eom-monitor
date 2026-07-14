from nicegui import ui
from src.frontend.api.client import LitestarApiClient
from src.frontend.services.device_service import DeviceService
from src.frontend.ui.viewmodels.edging_vm import EdgingGraphViewModel

class Edging:
    def __init__(self, client: LitestarApiClient, service: DeviceService):
        self.client = client
        self.service = service

    async def render(self):

        ui.label("Edging").classes("text-3xl")
        vm = EdgingGraphViewModel(self.service)

        with ui.card() as self.card:
            ui.label("Raw instant data").classes('font-bold')
            with ui.grid(columns=2).classes('gap-x-4 gap-y-2'):
                ui.label('Time since power on:')
                ui.label().bind_text_from(vm, 'time_since_power_on')

                ui.label('Pressure:')
                ui.label().bind_text_from(vm, 'pressure')

                ui.label('Arousal level:')
                ui.label().bind_text_from(vm, 'arousal_level')

                ui.label('Motor speed:')
                ui.label().bind_text_from(vm, 'motor_speed')

        return self.card