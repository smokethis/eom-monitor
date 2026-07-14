from nicegui import ui
from src.frontend.services.device_service import DeviceService

class InfoCard:

    def __init__(self, device: DeviceService):
        self.service = device
        self.card = None

    def render(self):

        with ui.card() as self.card:
            ui.label(
                f"Hostname: {self.service.device.name}"
            )

            ui.label(
                f"Arousal Threshold: {self.service.device.edging_controls.arousal_threshold}"
            )

            ui.label(
                f"Sensor Sensitivity: {self.service.device.edging_controls.sensor_sensitivity}"
            )

        return self.card