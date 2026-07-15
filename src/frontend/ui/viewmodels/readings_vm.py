from src.shared.device.device import Device

class ReadingsViewModel():
    def __init__(self, service):
        self.arousal_level = 0
        self.pressure = 0
        self.time_since_power_on = 0
        self.service = service

        service.subscribe(self.device_updated)
        
    def device_updated(self, device: Device):
        self.pressure = device.readings.pressure
        self.time_since_power_on = device.state.time_since_power_on
    
    def dispose(self):
        self.service.unsubscribe(self.device_updated)