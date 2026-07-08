from enum import Enum
import msgspec
from msgspec import Struct
from websocket import create_connection, WebSocket

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

class EdgeOMaticConfig(Struct):
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
    

class EdgeOMaticReadings(Struct):
    pressure: int
    pavg: int
    motor: int
    arousal: int
    millis: int
    run_mode: ControlMode = msgspec.field(name="runMode")

    # REMOVED IN firmware v2.0 broadcast.c
    # permit_orgasm: bool = msgspec.field(name="permitOrgasm")
    # post_orgasm: bool = msgspec.field(name="postOrgasm")
    # lock: bool

    # NEW FIELDS FROM firmware v2.0 broadcast.c:
    detect_state: str = msgspec.field(name="detectState")
    detect_baseline: int = msgspec.field(name="detectBaseline")
    detect_peak_count: int = msgspec.field(name="detectPeakCount")
    detect_sustained_ms: int = msgspec.field(name="detectSustainedMs")
    detect_last_interval_ms: int = msgspec.field(name="detectLastIntervalMs")

class EdgeOMaticInfo(Struct):
    device: str
    serial: str
    hw_version: str = msgspec.field(name="hwVersion")
    fw_version: str = msgspec.field(name="fwVersion")

class EdgeOMatic:
    ws: WebSocket
    _config: EdgeOMaticConfig

    @staticmethod
    def send_and_recv_struct(ws: WebSocket, struct: Struct, wait_for_name: str|None=None, type=object):
        ws.send(msgspec.json.encode(struct))
        if wait_for_name:
            while True:
                res = msgspec.json.decode(ws.recv(), type=object)
                if wait_for_name in res:
                    return msgspec.convert(res[wait_for_name], type)
        return msgspec.json.decode(ws.recv(), type=type)
    
    @staticmethod
    def recv_struct(ws: WebSocket, wait_for_name: str|None=None, type=object):
        if wait_for_name:
            while True:
                res = msgspec.json.decode(ws.recv(), type=object)
                if wait_for_name in res:
                    return msgspec.convert(res[wait_for_name], type)
        return msgspec.json.decode(ws.recv(), type=type)
    
    def __init__(self, ip: str, port: int):
        self.ws = create_connection(f"ws://{ip}:{port}/")
        self.send_and_recv_struct(self.ws, {
            "streamReadings": None
        })
        self._config = self.send_and_recv_struct(self.ws, {
            "configList": None
        }, wait_for_name="configList", type=EdgeOMaticConfig)

    @property
    def config(self) -> EdgeOMaticConfig:
        return self._config
    
    def set_config(self, config: EdgeOMaticConfig):
        self._config = config
        self.send_and_recv_struct(self.ws, {
            "configSet": dict(config)
        })

    def get_readings(self):
        return self.recv_struct(self.ws, "readings", EdgeOMaticReadings)
    
    def set_mode(self, mode: ControlMode):
        return self.send_and_recv_struct(self.ws, {
            "setMode": mode.value
        }, "setMode")
    
    def set_motor_speed(self, speed: int):
        return self.send_and_recv_struct(self.ws, {
            "setMotor": speed
        }, "setMotor")
    
    def restart(self):
        return self.send_and_recv_struct(self.ws, {
            "restart": None
        }, "restart")
    
    def get_info(self):
        return self.send_and_recv_struct(self.ws, {
            "info": None
        }, "info", EdgeOMaticInfo)
    
    def close(self):
        self.ws.close(timeout=None)