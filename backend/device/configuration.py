from .wifi import Wifi
from .bluetooth import Bluetooth
from .display import Display
from .webserver import Webserver
from .serial import Serial
from .console import Console
from dataclasses import dataclass, field

@dataclass
class Configuration():
    filename: str = ""
    language_file_name: str = ""
    remote_update_url: str = ""
    version: int = 0
    wifi: Wifi = field(default_factory=Wifi)
    bluetooth: Bluetooth = field(default_factory=Bluetooth)
    display: Display = field(default_factory=Display)
    webserver: Webserver = field(default_factory=Webserver)
    serial: Serial = field(default_factory=Serial)
    console: Console = field(default_factory=Console)

