from dataclasses import dataclass
from src.shared.models.modes import ControlMode, ConnectionState

@dataclass
class State():
    run_mode:ControlMode = ControlMode.Manual
    motor_speed:int = 0
    time_since_power_on:int = 0 # Milliseconds
    serial_connection:ConnectionState = ConnectionState.Disconnected
    websocket_connection:ConnectionState = ConnectionState.Disconnected

    def apply_patch(self, patch):
        for key, value in patch.items():
            setattr(self, key, value)