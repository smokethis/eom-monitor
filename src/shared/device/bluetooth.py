from dataclasses import dataclass

@dataclass
class Bluetooth():
    name: str = ""
    force_coexistence: bool = False
    enabled: bool = False
