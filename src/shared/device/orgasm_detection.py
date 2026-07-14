from dataclasses import dataclass

@dataclass
class OrgasmDetection():
    mode:int = 0
    sustained_threshold:int = 0
    sustained_fallback:int = 0 # Milliseconds
    sustained_dropout:int = 0 # Milliseconds
    peak_min_amplitude:int = 0
    rhythmic_min_peaks:int = 0
    rhythmic_interval_min:int = 0 # Milliseconds
    rhythmic_interval_max:int = 0 # Milliseconds
    rhythmic_interval_variance:int = 0 # Milliseconds
    rhythmic_timeout:int = 0 # Milliseconds
    arousal_gate_percent:int = 0
    recovery:int = 0 # Milliseconds
    clench_arousal_boost:bool = False
    clench_arousal_boost_amount:int= 0
    detection_armed:bool= False

    def apply_patch(self, patch):
        for key, value in patch.items():
            setattr(self, key, value)