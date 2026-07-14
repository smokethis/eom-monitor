from dataclasses import dataclass

@dataclass
class Wifi():
    ssid: str = ""
    password: str = ""
    enabled: bool = True
    hostname: str = ""

    def apply_patch(self, patch: dict[str, object]) -> None:
        for key, value in patch.items():
            setattr(self, key, value)