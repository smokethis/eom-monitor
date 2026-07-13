from shared.device.device import Device

class ReadingsViewModel():
    def __init__(self, service):
        self.arousal_level = 0
        self.pressure = 0
        self.time_since_power_on = 0
        self.service = service

        service.subscribe(self.device_updated)

    def device_updated(self, device: Device, patch):
        if "arousal_level" in patch:
            self.arousal_level = device.readings.arousal_level

        if "pressure" in patch:
            self.pressure = device.readings.pressure

        if "time_since_power_on" in patch:
            self.time_since_power_on = device.state.time_since_power_on
    
    def dispose(self):
        self.service.unsubscribe(self.device_updated)