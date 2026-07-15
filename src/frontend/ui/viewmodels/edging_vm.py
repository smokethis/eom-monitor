from src.shared.device.device import Device
from collections import deque
import time

class EdgingViewModel:
    def __init__(self, service):
        self.arousal_level = 0
        self.pressure = 0
        self.time_since_power_on = 0
        self.motor_speed = 0
        self.arousal_percent = 0
        self.motor_percent = 0
        self.service = service
        self.arousal_level_history = deque(maxlen=250)
        self.pressure_history = deque(maxlen=250)
        self.motor_speed_history = deque(maxlen=250)

        service.subscribe(self.device_updated)
        
    def device_updated(self, device: Device):
        # Update static elements
        self.pressure = (device.readings.pressure / 4095) * 100
        self.time_since_power_on = device.state.time_since_power_on
        self.motor_speed = device.state.motor_speed
        self.arousal_level = device.readings.arousal_level
        self.motor_percent = (device.state.motor_speed / device.edging_controls.motor_settings.max_speed) * 100
        self.arousal_percent = (device.readings.arousal_level / device.edging_controls.arousal_threshold) * 100

    def sample(self):
        now = time.time()

        # Update history deques
        # self.pressure_history.append((now, (device.readings.pressure / 4095) * 100))
        self.arousal_level_history.append((now, self.arousal_percent))
        self.motor_speed_history.append((now, self.motor_percent))

    def dispose(self):
        self.service.unsubscribe(self.device_updated)