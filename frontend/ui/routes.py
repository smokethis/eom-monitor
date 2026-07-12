from nicegui import ui
from .widgets.layout import Layout
from .pages.dashboard import Dashboard

def register_routes(device):

    # Root page
    @ui.page("/")
    async def index():
        
        layout = Layout()

        with layout.content:
            dashboard = Dashboard(device)
            await dashboard.render()

        ui.context.client.on_disconnect(dashboard.cleanup)
