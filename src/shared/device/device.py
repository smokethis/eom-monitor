from ..models.messages import ConfigMessage, InfoMessage, ReadingsMessage
from .configuration import Configuration
from .edging_controls import EdgingControls
from .console import Console
from .orgasm_detection import OrgasmDetection
from .readings import Readings
from .state import State
from dataclasses import dataclass, field
from collections import deque

class DeviceRaw():
    def __init__(self):
        self.configuration: ConfigMessage | None = None
        self.info: InfoMessage | None = None
        self.readings: ReadingsMessage
        self.readings_history = deque(maxlen=1000) # Should be enough for about the last 20 seconds at 50Hz

@dataclass
class Device():
    name: str = ""
    serial: str = ""
    hw_version: str = ""
    fw_version: str = ""
    configuration: Configuration = field(default_factory=Configuration)
    edging_controls: EdgingControls = field(default_factory=EdgingControls)
    console: Console = field(default_factory=Console)
    orgasm_detection: OrgasmDetection = field(default_factory=OrgasmDetection)
    state: State = field(default_factory=State)
    readings: Readings = field(default_factory=Readings)

    # def __init__(self):
    #     self.configuration = Configuration()
    #     self.edging_controls = EdgingControls()
    #     self.console = Console()
    #     self.name = ""
    #     self.serial = ""
    #     self.hw_version = ""
    #     self.fw_version = ""
    #     self.orgasm_detection = OrgasmDetection() # These are horrible and I hate them but I can't be arsed to fix them right now.
    #     self.state = State()

    def update_from_config(self, config: ConfigMessage):
        self.edging_controls.arousal_decay_rate = config.arousal_decay_rate
        self.edging_controls.arousal_detection_holdoff = config.arousal_holdoff_ms
        self.configuration.bluetooth.name = config.bt_display_name
        self.configuration.bluetooth.enabled = config.bt_on
        self.configuration.serial.use_classic = config.classic_serial
        self.configuration.console.basic_mode = config.console_basic_mode
        self.edging_controls.cooldown_delay = config.cooldown_delay_ms
        self.edging_controls.cooldown_randomised_additional_delay = config.cooldown_random_ms
        self.configuration.display.denial_count_mode = config.denial_count_mode
        self.configuration.display.screensaver = config.enable_screensaver
        self.configuration.bluetooth.force_coexistence = config.force_bt_coex
        self.configuration.wifi.hostname = config.hostname
        self.configuration.language_file_name = config.language_file_name
        self.configuration.display.brightness = config.led_brightness
        self.configuration.webserver.mdns = config.mdns_enabled
        self.edging_controls.motor_settings.max_speed = config.motor_max_speed
        self.edging_controls.motor_settings.min_speed = config.motor_min_speed
        self.edging_controls.motor_settings.ramp_time = config.motor_ramp_time_s
        self.orgasm_detection.arousal_gate_percent = config.od_arousal_gate_percent
        self.orgasm_detection.clench_arousal_boost = config.od_clench_arousal_boost
        self.orgasm_detection.clench_arousal_boost_amount = config.od_clench_arousal_boost_amount
        self.orgasm_detection.detection_armed = config.od_detection_armed
        self.orgasm_detection.mode = config.od_mode
        self.orgasm_detection.peak_min_amplitude = config.od_peak_min_amplitude
        self.orgasm_detection.recovery = config.od_recovery_ms
        self.orgasm_detection.rhythmic_interval_max = config.od_rhythmic_interval_max_ms
        self.orgasm_detection.rhythmic_interval_min = config.od_rhythmic_interval_min_ms
        self.orgasm_detection.rhythmic_interval_variance = config.od_rhythmic_interval_variance_ms
        self.orgasm_detection.rhythmic_min_peaks = config.od_rhythmic_min_peaks
        self.orgasm_detection.rhythmic_timeout = config.od_rhythmic_timeout_ms
        self.orgasm_detection.sustained_dropout = config.od_sustained_dropout_ms
        self.orgasm_detection.sustained_fallback = config.od_sustained_fallback_ms
        self.orgasm_detection.sustained_threshold = config.od_sustained_threshold
        self.edging_controls.pressure_smoothing = config.pressure_smoothing
        self.configuration.remote_update_url = config.remote_update_url
        self.configuration.display.reverse_scroll = config.reverse_menu_scroll
        self.configuration.display.dim_delay = config.screen_dim_seconds
        self.configuration.display.timeout_delay = config.screen_timeout_seconds
        self.edging_controls.arousal_threshold = config.sensitivity_threshold
        self.edging_controls.sensor_sensitivity = config.sensor_sensitivity
        self.configuration.console.store_command_history = config.store_command_history
        self.edging_controls.update_frequency = config.update_frequency_hz
        self.edging_controls.use_average_values = config.use_average_values
        self.configuration.webserver.ssl = config.use_ssl
        self.configuration.version = config.version
        self.edging_controls.motor_settings.vibration_mode = config.vibration_mode
        self.configuration.webserver.port = config.websocket_port
        self.configuration.wifi.password = config.wifi_key
        self.configuration.wifi.ssid = config.wifi_ssid
        self.configuration.wifi.enabled = config.wifi_on
        self.configuration.filename = config._filename
    
    def update_from_info(self, info: InfoMessage):
        self.name = info.device
        self.fw_version = info.fw_version
        self.hw_version = info.hw_version
        self.serial = info.serial

    def update_from_readings(self, readings: ReadingsMessage):
        self.readings.arousal_level = readings.arousal
        # self.? = readings.detect_baseline
        # self.? = readings.detect_sustained_ms
        # self.? = readings.detect_peak_count
        # self.? = readings.detect_state
        # self.? = readings.detect_sustained_ms
        self.state.time_since_power_on = readings.millis
        self.state.motor_speed = readings.motor
        self.readings.pressure_avg = readings.pavg
        self.readings.pressure = readings.pressure
        self.state.run_mode = readings.run_mode
