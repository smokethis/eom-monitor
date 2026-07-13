from dataclasses import dataclass

@dataclass
class Console():
    basic_mode: bool = False
    store_command_history: bool = False
