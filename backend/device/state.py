from ..eom.models import ControlMode

class State():
    def __init__(self):
        self.run_mode: ControlMode
        self.motor_speed = 0 # 0-4096?
        self.time_since_power_on = 0 # Milliseconds