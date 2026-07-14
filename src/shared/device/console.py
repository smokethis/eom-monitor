from dataclasses import dataclass

@dataclass
class Console():
    basic_mode: bool = False
    store_command_history: bool = False

    def apply_patch(self, patch: dict[str, object]) -> None:
        for key, value in patch.items():
            setattr(self, key, value)
