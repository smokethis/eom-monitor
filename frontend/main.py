from nicegui import ui
import json
from api.client import DeviceAPI
from services.event_stream import EventStream
from pages.dashboard import Dashboard
from pages.layout import Layout

client = DeviceAPI()
stream = EventStream()

# JSON data parser
def show_json(data):
    ui.code(
        json.dumps(data, indent=2),
        language="json"
    )

# Generic API display route
@ui.page("/api/{endpoint:path}")
async def api_viewer(endpoint: str):

    layout = Layout()

    with layout.content:
        ui.label(f"/api/{endpoint}").classes("text-3xl")

        data = await client.get_api(endpoint)

        show_json(data)

# Root page
@ui.page("/")
async def root():

    layout = Layout()

    with layout.content:
        dashboard = Dashboard(client, stream)
        await dashboard.render()

    ui.context.client.on_disconnect(
        dashboard.cleanup
    )

ui.run(
    host="0.0.0.0",
    port=8080
)