from nicegui import ui
from .widgets.title_bar import TitleBar
from .pages.dashboard import Dashboard
from .pages.edging import Edging
from src.shared.utils import serialisation
from dataclasses import asdict

def register_routes(client,service):

    # Root page
    @ui.page("/")
    async def index():
        title = TitleBar()
        with title.content:
            dashboard = Dashboard(client, service)
            dashboard.render()

        # This needs to come back but I can't be arsed right now.
        # ui.context.client.on_disconnect(dashboard.cleanup)
    
    # Edging page
    @ui.page("/edging")
    async def edging():
        title = TitleBar()
        with title.content:
            edging = Edging(client, service)
            edging.render()

    # Route and logic to retrieve serialised device state for debugging. It might be shit?
    @ui.page("/view/{path:path}")
    async def view_info(path: str):
        title = TitleBar()

        data = resolve_path(service, path)
        d2 = asdict(data)

        with title.content:
            ui.code(
                serialisation.pretty_json(service.device),
                language="json"
            )

    def resolve_path(obj, path: str):
        if not path:
            return obj

        for part in path.split("/"):
            obj = getattr(obj, part)

        return obj