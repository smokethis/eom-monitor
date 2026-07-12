from msgspec import Struct, field
from ..models.modes import VibrationMode, ControlMode

class ConfigMessage(Struct):
    wifi_ssid: str
    wifi_key: str
    wifi_on: bool
    bt_display_name: str
    bt_on: bool
    force_bt_coex: bool
    led_brightness: int
    websocket_port: int
    use_ssl: bool
    hostname: str
    motor_min_speed: int
    motor_max_speed: int
    motor_ramp_time_s: int
    cooldown_delay_ms: int
    cooldown_random_ms: int
    arousal_holdoff_ms: int
    screen_dim_seconds: int
    screen_timeout_seconds: int
    reverse_menu_scroll: bool
    pressure_smoothing: int
    classic_serial: bool
    sensitivity_threshold: int
    update_frequency_hz: int
    sensor_sensitivity: int
    use_average_values: bool
    vibration_mode: VibrationMode
    # ADDED FROM v2.0 firmware config file
    _filename: str
    store_command_history: bool
    console_basic_mode: bool
    enable_screensaver: bool
    language_file_name: str
    remote_update_url: str
    version: int = field(name="$version")
    mdns_enabled: bool
    denial_count_mode: int
    arousal_decay_rate: int
    od_mode: int
    od_sustained_threshold: int
    od_sustained_fallback_ms: int
    od_sustained_dropout_ms: int
    od_peak_min_amplitude: int
    od_rhythmic_min_peaks: int
    od_rhythmic_interval_min_ms: int
    od_rhythmic_interval_max_ms: int
    od_rhythmic_interval_variance_ms: int
    od_rhythmic_timeout_ms: int
    od_arousal_gate_percent: int
    od_recovery_ms: int
    od_clench_arousal_boost: bool
    od_clench_arousal_boost_amount: int
    od_detection_armed: bool

class ReadingsMessage(Struct):
    pressure: int
    pavg: int
    motor: int
    arousal: int
    millis: int
    run_mode: ControlMode = field(name="runMode")

    # REMOVED IN firmware v2.0 broadcast.c
    # permit_orgasm: bool = msgspec.field(name="permitOrgasm")
    # post_orgasm: bool = msgspec.field(name="postOrgasm")
    # lock: bool

    # NEW FIELDS FROM firmware v2.0 broadcast.c:
    detect_state: str = field(name="detectState")
    detect_baseline: int = field(name="detectBaseline")
    detect_peak_count: int = field(name="detectPeakCount")
    detect_sustained_ms: int = field(name="detectSustainedMs")
    detect_last_interval_ms: int = field(name="detectLastIntervalMs")

class InfoMessage(Struct):
    device: str
    serial: str
    hw_version: str = field(name="hwVersion")
    fw_version: str = field(name="fwVersion")

class WifiStatusMessage(Struct):
    ssid: str
    ip: str
    rssi: int
