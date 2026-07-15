from contextlib import contextmanager
from nicegui import ui
from src.frontend.ui.theme.styles import Theme

def title_bar(title):
    with ui.row().classes(Theme.TITLE_BAR):
        ui.label(title).classes(Theme.TITLE)

@contextmanager
def page_layout(title: str):
    """
    Creates the standard page container.
    """

    with ui.column().classes(
        "w-full min-h-screen bg-slate-950"
    ):

        title_bar(title)

        with ui.column().classes(
            "w-full flex-grow p-6 gap-4"
        ):
            yield