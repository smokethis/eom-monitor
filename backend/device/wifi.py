from dataclasses import dataclass

@dataclass
class Wifi():
    ssid: str = ""
    password: str = ""
    enabled: bool = True
    hostname: str = ""
