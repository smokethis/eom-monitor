from dataclasses import dataclass
from backend.models.modes import ControlMode

@dataclass
class State():
    run_mode:ControlMode = ControlMode.Manual
    motor_speed:int = 0 # 0-4096?
    time_since_power_on:int = 0 # Milliseconds