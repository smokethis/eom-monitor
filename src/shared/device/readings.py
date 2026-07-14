from dataclasses import dataclass

@dataclass
class Readings():
    pressure_avg:int = 0 # 0-4096 ?
    pressure:int = 0 # 0-4096?
    arousal_level:int = 0 # ??
    ### These are still sent in the event stream, but I'm not sure what they're actually trying to represent. They don't seem to appear in the source any more either.
    # detect_state: str
    # detect_baseline: int
    # detect_peak_count: int
    # detect_sustained_ms: int
    # detect_last_interval_ms: int

    def apply_patch(self, patch):
        for key, value in patch.items():
            setattr(self, key, value)