from nicegui import ui
from src.frontend.api.client import LitestarApiClient
from src.frontend.services.device_service import DeviceService
from src.frontend.ui.viewmodels.edging_vm import EdgingViewModel

class Edging:
    def __init__(self, client: LitestarApiClient, service: DeviceService):
        self.client = client
        self.service = service
        self.vm = EdgingViewModel(self.service)
    
    def render(self):
        ui.label("Edging").classes("text-3xl")
        with ui.column().classes("w-full"):
            with ui.row().classes("gap-4"):
                with ui.card().classes("w-64"):
                    self.textbox()
                with ui.card().classes("w-64"):
                    self.motor_gauge()
                with ui.card().classes("w-64"):
                    self.arousal_gauge()
            self.poc_graph()
        ui.timer(1/10, self.redraw_chart)

    def textbox(self):
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
    
    def motor_gauge(self):
        options = {
            "animationDurationUpdate": 200,
            "animationEasingUpdate": "linear",
            "series": [
                {
                    "type": "gauge",
                    "min": 0,
                    "max": 255,
                    "progress": {
                        "show": True,
                        "width": 18
                    },
                    "axisLine": {
                        "lineStyle": {
                            "width": 18
                        }
                    },
                    "axisTick": {
                        "show": False
                    },
                    "splitLine": {
                        "length": 15,
                        "lineStyle": {
                        "width": 2,
                        "color": '#999'
                        }
                    },
                    "axisLabel": {
                        "show": False
                    },
                    "anchor": {
                        "show": True,
                        "showAbove": True,
                        "size": 25,
                        "itemStyle": {
                        "borderWidth": 10
                        }
                    },
                    "detail": {
                        "valueAnimation": False
                    },
                    "data": []
                }
            ]
        }
        self.mg = ui.echart(options)
        return self.mg

    def arousal_gauge(self):
        options = {
            "animationDurationUpdate": 200,
            "animationEasingUpdate": "linear",
            "series": [
                {
                    "type": "gauge",
                    "startAngle": 180,
                    "endAngle": 0,
                    "center": ['50%', '75%'],
                    "radius": '90%',
                    "min": 0,
                    "max": 4096,
                    "splitNumber": 8,
                    "axisLine": {
                        "lineStyle": {
                        "width": 6,
                        "color": [
                            [0.25, '#7CFFB2'],
                            [0.5, '#58D9F9'],
                            [0.75, '#FDDD60'],
                            [1, '#FF6E76']
                            ]
                        }
                    },
                    "pointer": {
                    "icon": 'path://M12.8,0.7l12,40.1H0.7L12.8,0.7z',
                    "length": '12%',
                    "width": 20,
                    "offsetCenter": [0, '-60%'],
                    "itemStyle": {
                        "color": 'auto'
                        }
                    },
                    "axisTick": {
                        "length": 12,
                        "lineStyle": {
                        "color": 'auto',
                        "width": 2
                        }
                    },
                    "splitLine": {
                        "length": 20,
                        "lineStyle": {
                        "color": 'auto',
                        "width": 5
                        }
                    },
                    "axisLabel": {
                        "show": False
                        # "color": '#464646',
                        # "fontSize": 20,
                        # "distance": -60,
                        # "rotate": 'tangential',
                        # "formatter": function (value) {
                        # if (value === 0.875) {
                        #     return 'Grade A';
                        # } else if (value === 0.625) {
                        #     return 'Grade B';
                        # } else if (value === 0.375) {
                        #     return 'Grade C';
                        # } else if (value === 0.125) {
                        #     return 'Grade D';
                        # }
                        # return '';
                        # }
                    },
                    "title": {
                        "offsetCenter": [0, '-10%'],
                        "fontSize": 20
                    },
                    "detail": {
                        "fontSize": 30,
                        "offsetCenter": [0, '-35%'],
                        "valueAnimation": False,
                        # "formatter": function (value) {
                        # return Math.round(value * 100) + '';
                        # },
                        "color": 'inherit'
                    },
                    "data": []
                }
            ]
        }
        self.ag = ui.echart(options)
        return self.ag

    def poc_graph(self):
        options = {
            "title": {
                "text": "Edging"
            },
            "xAxis": {
                "type": "time",
                "data": [],
                "minorTick": {
                    "show": True
                },
                "splitLine": {
                    "lineStyle": {
                        "color": "#999"
                    }
                },
                "minorSplitLine": {
                    "show": True,
                    "lineStyle": {
                        "color": "#ddd"
                    }
                }
            },
            "legend": {},
            "yAxis": [
                    {
                        "type": "value",
                        "name": "bignumber",
                        "min": "0",
                        "max": "4096",
                        "position": "left"
                    },
                    {
                        "type": "value",
                        "name": "smallnumber",
                        "min": 0,
                        "max": 255,
                        "position": "right"
                    },

            ],
            "series": [
                {
                    "name": "Pressure",
                    "type": "line",
                    "data": [],
                    "yAxisIndex": 0
                },
                {
                    "name": "Arousal level",
                    "type": "line",
                    "data": [],
                    "yAxisIndex": 0
                },
                {
                    "name": "Motor speed",
                    "type": "line",
                    "data": [],
                    "yAxisIndex": 1
                }
            ],
        }

        self.chart = ui.echart(options).classes("h-96")
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
        self.mg.run_chart_method(
            "setOption",
            {
                "series": [
                    {
                        "data": [
                            {
                                "value": self.vm.motor_speed
                            }
                        ]
                    }
                ]
            }
        )
        self.ag.run_chart_method(
            "setOption",
                {
                "series": [
                    {
                        "data": [
                            {
                                "value": self.vm.arousal_level
                            }
                        ]
                    }
                ]
            }
        )