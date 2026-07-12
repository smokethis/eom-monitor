class Readings():
    def __init__(self):
        self.pressure_avg = 0 # 0-4096 ?
        self.pressure = 0 # 0-4096?
        self.arousal_level = 0 # ??
        ### These are still sent in the event stream, but I'm not sure what they're actually trying to represent. They don't seem to appear in the source any more either.
        # detect_state: str
        # detect_baseline: int
        # detect_peak_count: int
        # detect_sustained_ms: int
        # detect_last_interval_ms: int

