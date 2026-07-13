from dataclasses import dataclass

@dataclass
class Webserver():
    port: int = 0
    ssl: bool = False
    hostname: str = ""
    mdns: bool = False
