from nicegui import ui

class LiveLineChart:

    def __init__(self, title="", x_label="", y_label="", max_points=100):
        self.options = {
            "title": {"text": title},
            "xAxis": {
                "type": "category",
                "name": x_label,
                "data": [],
            },
            "yAxis": {
                "type": "value",
                "name": y_label,
            },
            "series": [],
        }
        self.series = {}
        self.max_points = max_points
        self.chart = None

    def add_series(self, name: str, *, colour=None, smooth=False):
        series = {
            "name": name,
            "type": "line",
            "data": [],
            "smooth": smooth,
        }

        if colour:
            series["lineStyle"] = {"color": colour}
            series["itemStyle"] = {"color": colour}

        self.series[name] = series
        self.options["series"].append(series)

        return self

    def render(self):
        self.chart = ui.echart(self.options)
        return self

    def add_point(self, series_name, x, y):
        self.options["xAxis"]["data"].append(x)
        self.series[series_name]["data"].append(y)

        if len(self.options["xAxis"]["data"]) > self.max_points:
            self.options["xAxis"]["data"].pop(0)
            for series in self.options["series"]:
                series["data"].pop(0)

        self.chart.update()