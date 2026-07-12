from enum import Enum

class ControlMode(Enum):
    Manual = "MANUAL_CONTROL"
    Automatic = "AUTOMAITC_CONTROL" # Yes its spelled incorrectly in the device code :)
    Orgasm = "ORGASM_MODE"
    Unk = ""
    
class VibrationMode(Enum):
    GlobalSync = 0
    RampStop = 1
    Depletion = 2
    Enhancement = 3