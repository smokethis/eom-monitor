from ..eom.models import VibrationMode

class Motor():
    def __init__(self):
        self.min_speed = 0
        self.max_speed = 0
        self.ramp_time = 0 # Seconds
        self.vibration_mode: VibrationMode
