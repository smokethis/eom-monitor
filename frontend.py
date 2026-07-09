from nicegui import ui
import httpx
import json

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

@ui.page("/api/{endpoint:path}")
async def api_viewer(endpoint: str):

    ui.label(f"/api/{endpoint}").classes("text-3xl")

    data = await api_get(f"/api/{endpoint}")

    show_json(data)

ui.run(
    host="0.0.0.0",
    port=8080
)