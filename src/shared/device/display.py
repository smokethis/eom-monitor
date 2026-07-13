from dataclasses import dataclass

@dataclass
class Display():
    brightness: int = 0
    dim_delay: int = 0 # Seconds
    timeout_delay: int = 0 # Seconds
    screensaver: bool = False
    reverse_scroll: bool = False
    denial_count_mode: int = 0
