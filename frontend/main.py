from nicegui import ui
import httpx
import json
import asyncio
from api.client import DeviceAPI

client = DeviceAPI()

# JSON data parser
def show_json(data):
    ui.code(
        json.dumps(data, indent=2),
        language="json"
    )

# Event listener
async def listen_for_events(on_event):

    async with httpx.AsyncClient(timeout=None) as client:

        async with client.stream("GET", f"{LITESTAR_BASE}/api/events") as response:

            async for line in response.aiter_lines():

                if line.startswith("data:"):

                    payload = line[5:].strip()

                    if payload:
                        await on_event(
                            json.loads(payload)
                        )

# Generic API display route
@ui.page("/api/{endpoint:path}")
async def api_viewer(endpoint: str):

    ui.label(f"/api/{endpoint}").classes("text-3xl")

    data = await api_get(f"/api/{endpoint}")

    show_json(data)

# Root page
@ui.page("/")
async def root():

    ui.label("Dashboard").classes("text-3xl")

    config = await client.get_config()

    alive = True

    async def start_events():
        ui.notify("Starting event stream...")
        await client.start_readings()

    async def restart_device():
        ui.notify("Restarting device...")
        await client.restart()

    with ui.row():
        ui.button('Start stream', on_click=lambda: start_events())
        ui.button('Restart device', on_click=lambda: restart_device())

    with ui.row():
        with ui.card():
            ui.label(f"Hostname: {config['hostname']}")
            ui.label(f"Arousal Threshold: {config['sensitivity_threshold']}")
            ui.label(f"Sensor Sensitivity: {config['sensor_sensitivity']}")

        latest_event = ui.code("Waiting for events...", language="json")

    async def handle_event(event):

        if not alive:
            return
            
        with latest_event:
            latest_event.content = json.dumps(event, indent=2)
            latest_event.update()
    
    task = asyncio.create_task(listen_for_events(handle_event))

    def cleanup():
        nonlocal alive

        alive = False
        task.cancel()

    ui.context.client.on_disconnect(cleanup)

ui.run(
    host="0.0.0.0",
    port=8080
)