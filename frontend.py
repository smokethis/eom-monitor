from nicegui import ui
import httpx
import json
import asyncio

LITESTAR_BASE = "http://localhost:8000/"

async def api_get(path):
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{LITESTAR_BASE}{path}")

        if response.is_error:
            return {
                "status": response.status_code,
                "error": response.text
            }

        return response.json()

def show_json(data):
    ui.code(
        json.dumps(data, indent=2),
        language="json"
    )

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

@ui.page("/api/{endpoint:path}")
async def api_viewer(endpoint: str):

    ui.label(f"/api/{endpoint}").classes("text-3xl")

    data = await api_get(f"/api/{endpoint}")

    show_json(data)

@ui.page("/")
async def root():

    ui.label("Dashboard").classes("text-3xl")

    config = await api_get("/api/config")

    alive = True

    with ui.card():
        ui.label(f"Hostname: {config['hostname']}")
        ui.label(f"Arousal Threshold: {config['sensitivity_threshold']}")
        ui.label(f"Sensor Sensitivity: {config['sensor_sensitivity']}")

    events = ui.column()

    async def handle_event(event):

        if not alive:
            return
        
        with events:
            ui.label(json.dumps(event))
    
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