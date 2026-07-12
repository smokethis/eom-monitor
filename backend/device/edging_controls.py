from .motor import Motor

class EdgingControls():
    def __init__(self):
        self.cooldown_delay = 0 # Milliseconds
        self.cooldown_randomised_additional_delay = 0 # Milliseconds
        self.arousal_detection_holdoff = 0 # Milliseconds
        self.pressure_smoothing = 0 # Unknown
        self.arousal_threshold = 0 # 0-256 ?
        self.sensor_sensitivity = 0 # 0-4096 ?
        self.use_average_values = False
        self.update_frequency = 50 # Hz
        self.arousal_decay_rate = 0 # ?
        self.run_mode = ""
        self.motor_settings = Motor()
