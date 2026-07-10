from nicegui import ui

class ConfigCard:

    def __init__(self, config):
        self.config = config
        self.card = None

    def render(self):

        with ui.card() as self.card:
            ui.label(
                f"Hostname: {self.config['hostname']}"
            )

            ui.label(
                f"Arousal Threshold: {self.config['sensitivity_threshold']}"
            )

            ui.label(
                f"Sensor Sensitivity: {self.config['sensor_sensitivity']}"
            )

        return self.card