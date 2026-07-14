from nicegui import ui

class EdgingChart():
    def __init__(self):
        self.x_values = []
        self.y_values = []

        self.chart = ui.echart({
            "xAxis": {
                "type": "category",
                "data": self.x_values,
            },
            "yAxis": {
                "type": "value",
            },
            "series": [
                {
                    "type": "line",
                    "data": self.y_values,
                }
            ],
        })
        self.counter = 0

    def tick(self):

        self.x_values.append(self.counter)
        self.y_values.append(self.counter ** 2)

        if len(self.x_values) > 50:
            self.x_values.pop(0)
            self.y_values.pop(0)

        self.chart.update()
        self.counter += 1


    ui.timer(0.1, tick)