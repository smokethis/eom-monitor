from src.shared.device.device import Device
from collections import deque

class EdgingViewModel():
    def __init__(self, service):
        self.arousal_level = 0
        self.pressure = 0
        self.time_since_power_on = 0
        self.motor_speed = 0
        self.service = service
        self.arousal_level_history = deque(maxlen=1000)
        self.pressure_history = deque(maxlen=1000)
        self.motor_speed_history = deque(maxlen=1000)

        service.subscribe(self.device_updated)
        
    def device_updated(self, device: Device):
        # Update static elements
        self.pressure = device.readings.pressure
        self.time_since_power_on = device.state.time_since_power_on
        self.motor_speed = device.state.motor_speed
        self.arousal_level = device.edging_controls.arousal_threshold

        # Update history deques
        self.pressure_history.append((device.state.time_since_power_on, device.readings.pressure))
        self.arousal_level_history.append((device.state.time_since_power_on, device.readings.arousal_level))
        self.motor_speed_history.append((device.state.time_since_power_on, device.state.motor_speed))
    
    def dispose(self):
        self.service.unsubscribe(self.device_updated)