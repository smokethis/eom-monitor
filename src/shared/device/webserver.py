from dataclasses import dataclass

@dataclass
class Webserver():
    port: int = 0
    ssl: bool = False
    hostname: str = ""
    mdns: bool = False

    def apply_patch(self, patch: dict[str, object]) -> None:
        for key, value in patch.items():
            setattr(self, key, value)