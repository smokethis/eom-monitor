import httpx
from msgspec import Struct
import msgspec
from enum import Enum

LITESTAR_BASE = "http://localhost:8000/"

# Generic API GET function
async def api_get(path):
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{LITESTAR_BASE}{path}")

        if response.is_error:
            return {
                "status": response.status_code,
                "error": response.text
            }

        return response.json()

# Generic API POST function
async def api_post(path):
    async with httpx.AsyncClient() as client:
        response = await client.post(f"{LITESTAR_BASE}{path}")

        if response.is_error:
            return {
                "status": response.status_code,
                "error": response.text
            }

class ControlMode(Enum):
    Manual = "MANUAL_CONTROL"
    Automatic = "AUTOMAITC_CONTROL"
    Orgasm = "ORGASM_MODE"
    Unk = ""

class VibrationMode(Enum):
    GlobalSync = 0
    RampStop = 1
    Depletion = 2
    Enhancement = 3

class DeviceConfig(Struct):
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
    version: int = msgspec.field(name="$version")
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

class DeviceAPI:
    def __init__(self):
        self.base_uri = LITESTAR_BASE

    async def get_config(self):
        return await api_get("/api/config")

    async def restart(self):
        return await api_post("/api/restart")

    async def start_stream(self):
        return await api_post("/api/start_stream")
    
    async def get_api(self, endpoint):
        return await api_get(f"/api/{endpoint}")