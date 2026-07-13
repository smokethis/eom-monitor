from nicegui import ui
from frontend.api.client import LitestarApiClient

class InfoCard:

    def __init__(self, client: LitestarApiClient):
        self.client = client
        self.card = None

    def render(self):

        with ui.card() as self.card:
            ui.label(
                f"Hostname: {self.device.name}"
            )

            ui.label(
                f"Arousal Threshold: {self.device.edging_controls.arousal_threshold}"
            )

            ui.label(
                f"Sensor Sensitivity: {self.device.edging_controls.sensor_sensitivity}"
            )

        return self.card