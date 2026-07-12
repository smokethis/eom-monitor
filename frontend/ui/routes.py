from nicegui import ui
from .widgets.layout import Layout
from .pages.dashboard import Dashboard

def register_routes(client):

    # Root page
    @ui.page("/")
    async def index():
        
        layout = Layout()

        with layout.content:
            dashboard = Dashboard(client)
            await dashboard.render()

        ui.context.client.on_disconnect(dashboard.cleanup)
