from dataclasses import dataclass

@dataclass
class Bluetooth():
    name: str = ""
    force_coexistence: bool = False
    enabled: bool = False

    def apply_patch(self, patch: dict[str, object]) -> None:
        for key, value in patch.items():
            setattr(self, key, value)