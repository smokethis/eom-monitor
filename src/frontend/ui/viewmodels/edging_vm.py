from src.shared.device.device import Device

class EdgingGraphViewModel():
    def __init__(self, service):
        self.arousal_level = 0
        self.pressure = 0
        self.time_since_power_on = 0
        self.motor_speed = 0
        self.service = service

        service.subscribe(self.device_updated)

    # def device_updated(self, device: Device, patch):
    #     print("device_updated fired: %s", patch)
    #     if "arousal_level" in patch["readings"]:
    #         self.arousal_level = device.readings.arousal_level

    #     if "pressure" in patch["readings"]:
    #         self.pressure = device.readings.pressure

    #     if "time_since_power_on" in patch["state"]:
    #         self.time_since_power_on = device.state.time_since_power_on
            # print("ViewModel Update: time_since_power_on now %s", self.time_since_power_on)
        
    def device_updated(self, device: Device):
        self.pressure = device.readings.pressure
        self.time_since_power_on = device.state.time_since_power_on
        self.motor_speed = device.state.motor_speed
        self.arousal_level = device.edging_controls.arousal_threshold
    
    def dispose(self):
        self.service.unsubscribe(self.device_updated)