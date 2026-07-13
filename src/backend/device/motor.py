from dataclasses import dataclass
from ..models.modes import VibrationMode

@dataclass
class Motor():
    min_speed: int = 0
    max_speed: int = 0
    ramp_time: int = 0 # Seconds
    vibration_mode: VibrationMode = VibrationMode.RampStop