from dataclasses import dataclass
from src.backend.models.modes import VibrationMode

@dataclass
class Motor():
    min_speed: int = 0
    max_speed: int = 255
    ramp_time: int = 0 # Seconds
    vibration_mode: VibrationMode = VibrationMode.RampStop

    def apply_patch(self, patch: dict[str, object]) -> None:
        for key, value in patch.items():
            setattr(self, key, value)