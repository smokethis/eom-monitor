from dataclasses import dataclass

@dataclass
class Serial():
    use_classic: bool = False

    def apply_patch(self, patch: dict[str, object]) -> None:
        for key, value in patch.items():
            setattr(self, key, value)