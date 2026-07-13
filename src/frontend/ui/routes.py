from nicegui import ui
from .widgets.layout import Layout
from .pages.dashboard import Dashboard
import json
from dataclasses import asdict
from enum import Enum

class EnumEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Enum):
            return obj.name
        return super().default(obj)

def register_routes(client,service):

    # Root page
    @ui.page("/")
    async def index():
        layout = Layout()
        with layout.content:
            dashboard = Dashboard(client, service)
            await dashboard.render()

        # This needs to come back but I can't be arsed right now.
        # ui.context.client.on_disconnect(dashboard.cleanup)

    @ui.page("/view/{path:path}")
    async def view_info(path: str):
        layout = Layout()

        data = resolve_path(service, path)
        d2 = asdict(data)

        with layout.content:
            ui.code(
                json.dumps(d2, indent=2, cls=EnumEncoder),
                language="json"
            )

    def resolve_path(obj, path: str):
        if not path:
            return obj

        for part in path.split("/"):
            obj = getattr(obj, part)

        return obj