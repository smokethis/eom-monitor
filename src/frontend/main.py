from nicegui import ui
from frontend.ui.routes import register_routes
from frontend.api.client import LitestarApiClient

client = LitestarApiClient()
register_routes(client)

ui.run(
    host="0.0.0.0",
    port=8080
)