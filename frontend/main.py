from nicegui import ui
from ui.routes import register_routes
from api.client import LitestarApiClient

async def main():

    client = LitestarApiClient()
    register_routes(client)

    ui.run(
        host="0.0.0.0",
        port=8080
    )