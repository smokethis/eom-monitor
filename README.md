# EdgeOMatic Control API

A Python-based REST API for controlling and monitoring EdgeOMatic devices via WebSockets.

## 🚀 Features

- Complete WebSocket communication with EdgeOMatic devices
- RESTful API endpoints for device control
- Configuration management
- Real-time readings and monitoring
- Multiple control modes (Manual, Automatic, Orgasm)
- Device information retrieval

## 📋 Requirements

- Python 3.14+
- `msgspec` library
- `websockets` library
- `litestar` web framework
- `nicegui` front end
- `httpx` used by nicegui

## Fixes
- Migrated the project to `websockets` - the upstream repository used websocket-client which isn't very good at asynchronous operation.
- Refactored all websocket routines to be non-blocking.
- Updated the schema of responses to be firmware v2.0.0 compliant.
- Refactored the API endpoints to be more understandable.
- Added a rudimentary `nicegui` front end to visualise data being exposed by Litestar.
- Defended against race condition in the EOM 3000 websocket handler (see known issues).

## Known Issues
- I've traced the source of the connection refusal behaviour; its a result of a race condition in the EOM websocket_handler.c. Once a streaming broadcast has been initiated, sending any other data-producing request to the device has a chance to produce an invalid websocket frame; in short websocket_handler.c can produce a "nested" response (header1, header2, payload2, payload1) which is illegal and a 1002 gets sent to the device immediatley to terminate the connection which is standard practice with a corrupt stream.
There is never an acknowledgement to the 1002 though which is suspicious; I wonder if the old connection isn't being cleaned up properly from that termination even though you can launch a new one shortly after, and you eventually get resource exhaustion and the HTTP server falls over.
- To protect against this unintended behaviour, this app has been programmed to never issue a "bad" request to the websocket connection once a stream has commenced. To terminate the stream the device must be reset.
- The EOM 3000 doesn't appear to respond to websocket commands like close properly. They appear to work but no response is ever generated. This still needs further investigation, for now best approach is to issue a device reset when wanting to return to a known good state.

## 🚀 Quick Start

1. Configure your EdgeOMatic device IP and port in `eom.py`:
```python
eom: EdgeOMatic = EdgeOMatic("your_device_ip", your_device_port)
```

2. Start the API server:

```bash
litestar --app backend:app run
```

3. Access the API at `http://localhost:8000`

## 🔌 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/config` | GET | Retrieve current device configuration |
| `/config` | POST | Update device configuration |
| `/readings` | GET | Get real-time device readings |
| `/mode/{mode}` | POST | Set the control mode (MANUAL_CONTROL, AUTOMAITC_CONTROL, ORGASM_MODE) |
| `/motor/{speed}` | POST | Set the motor speed (0-255) |
| `/restart` | POST | Restart the device |
| `/info` | GET | Get device information |

## 💡 Usage Examples

### Get Device Configuration

```bash
curl http://localhost:8000/config
```

### Update Configuration

```bash
curl -X POST http://localhost:8000/config \
  -H "Content-Type: application/json" \
  -d '{"motor_max_speed": 200, "sensitivity_threshold": 50, ...}'
```

### Get Current Readings

```bash
curl http://localhost:8000/readings
```

### Set Control Mode

```bash
curl -X POST http://localhost:8000/mode/XXX
```

### Set Motor Speed

```bash
curl -X POST http://localhost:8000/motor/XXX
```

## 🧠 Core Components

### EdgeOMatic Class

The `EdgeOMatic` class in `eom.py` provides the foundation for device communication:

- WebSocket connection management
- Configuration retrieval and updates
- Real-time readings
- Control mode selection
- Motor speed control

### REST API

Built with Litestar, the API in `rest.py` offers a user-friendly interface to interact with the device from any HTTP client.

## ⚠️ Important Notes

- This API is intended for controlling EdgeOMatic devices on a secure, private network.
- Always ensure proper device cleaning and maintenance according to the manufacturer's instructions.

---

*This project is not affiliated with EdgeOMatic's manufacturer and is provided as-is without warranty.*
