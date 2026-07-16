from contextlib import contextmanager
from nicegui import ui

def title_bar(title):
    with ui.row().classes():
        ui.label(title).classes("text-h3 text-bold")

@contextmanager
def page_layout(title: str):
    """
    Creates the standard page container.
    """

    # Disable dark mode, same theme no matter what
    ui.add_head_html('<meta name="darkreader-lock">')

    with ui.column().classes("w-full"):

        title_bar(title)

        with ui.column().classes("w-full"):
            yield