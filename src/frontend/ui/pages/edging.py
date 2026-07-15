from nicegui import ui
from src.frontend.api.client import LitestarApiClient
from src.frontend.services.device_service import DeviceService
from src.frontend.ui.viewmodels.edging_vm import EdgingViewModel
from collections import deque

class Edging:
    def __init__(self, client: LitestarApiClient, service: DeviceService):
        self.client = client
        self.service = service
        self.vm = EdgingViewModel(self.service)
    
    def render(self):
        ui.label("Edging").classes("text-3xl")
        self.textbox()
        self.poc_graph()
        ui.timer(1/20, self.redraw_chart)

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
                "text": "Edging",
            },
            "xAxis": {
                "type": "time",
                "data": [],
            },
            "yAxis": {
                "type": "value",
            },
            "series": [
                {
                    "name": "Pressure",
                    "type": "line",
                    "data": []
                },
                {
                    "name": "Arousal level",
                    "type": "line",
                    "data": []
                },
                {
                    "name": "Motor speed",
                    "type": "line",
                    "data": []
                }
            ],
        }

        self.chart = ui.echart(options)
        return self.chart
    
    def redraw_chart(self):
        self.chart.run_chart_method(
            "setOption",
            {
                "series": [
                    {"data": list(self.vm.pressure_history)},
                    {"data": list(self.vm.arousal_level_history)},
                    {"data": list(self.vm.motor_speed_history)}
                ]
            }
        )