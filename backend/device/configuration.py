from .wifi import Wifi
from .bluetooth import Bluetooth
from .display import Display
from .webserver import Webserver
from .serial import Serial
from .console import Console

class Configuration():
    def __init__(self):
        self.wifi = Wifi()
        self.bluetooth = Bluetooth()
        self.display = Display()
        self.webserver = Webserver()
        self.serial = Serial()
        self.console = Console()
        self.filename = ""
        self.language_file_name = ""
        self.remote_update_url = ""
        self.version = 0
