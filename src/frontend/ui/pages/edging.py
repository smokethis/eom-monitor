from nicegui import ui
from src.frontend.api.client import LitestarApiClient
from src.frontend.services.device_service import DeviceService
from src.frontend.ui.viewmodels.edging_vm import EdgingGraphViewModel
from src.frontend.ui.widgets.edging_chart import EdgingChart

class Edging:
    def __init__(self, client: LitestarApiClient, service: DeviceService):
        self.client = client
        self.service = service
        self.vm = EdgingGraphViewModel(self.service)
    
    def render(self):
        ui.label("Edging").classes("text-3xl")
        self.textbox()
        self.poc_graph()

    def textbox(self):
        with ui.card() as self.card:
            ui.label("Raw instant data").classes('font-bold')
            with ui.grid(columns=2).classes('gap-x-4 gap-y-2'):
                ui.label('Time since power on:')
                ui.label().bind_text_from(self.vm, 'time_since_power_on')

                ui.label('Pressure:')
                ui.label().bind_text_from(self.vm, 'pressure')

                ui.label('Arousal level:')
                ui.label().bind_text_from(self.vm, 'arousal_level')

                ui.label('Motor speed:')
                ui.label().bind_text_from(self.vm, 'motor_speed')

    def poc_graph(self):
        options = {
            "title": {
                "text": "Motor speed",
            },
            "xAxis": {
                "type": "category",
                "data": [5, 90, 56],
            },
            "yAxis": {
                "type": "value",
            },
            "series": [
                {
                    "name": "RPM",
                    "type": "line",
                    "data": [15, 25, 222],
                }
            ],
        }

        chart = ui.echart(options)
        return chart

        
