from .motor import Motor
from dataclasses import dataclass, field

@dataclass
class EdgingControls():
    cooldown_delay: int = 0 # Milliseconds
    cooldown_randomised_additional_delay: int = 0 # Milliseconds
    arousal_detection_holdoff: int = 0 # Milliseconds
    pressure_smoothing: int = 0 # Unknown
    arousal_threshold: int = 0 # 0-256 ?
    sensor_sensitivity: int = 0 # 0-4096 ?
    use_average_values: bool = False
    update_frequency: int = 50 # Hz
    arousal_decay_rate: int = 0 # ?
    run_mode:str = ""
    motor_settings:Motor = field(default_factory=Motor)

    def apply_patch(self, patch: dict[str, object]) -> None:
        for key, value in patch.items():
            current = getattr(self, key)

            if hasattr(current, "apply_patch") and isinstance(value, dict):
                current.apply_patch(value)
            else:
                setattr(self, key, value)