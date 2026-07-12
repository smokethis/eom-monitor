class OrgasmDetection():
    def __init__(self):
        self.mode = 0
        self.sustained_threshold = 0
        self.sustained_fallback = 0 # Milliseconds
        self.sustained_dropout = 0 # Milliseconds
        self.peak_min_amplitude = 0
        self.rhythmic_min_peaks = 0
        self.rhythmic_interval_min = 0 # Milliseconds
        self.rhythmic_interval_max = 0 # Milliseconds
        self.rhythmic_interval_variance = 0 # Milliseconds
        self.rhythmic_timeout = 0 # Milliseconds
        self.arousal_gate_percent = 0
        self.recovery = 0 # Milliseconds
        self.clench_arousal_boost = False
        self.clench_arousal_boost_amount = 0
        self.detection_armed = False
