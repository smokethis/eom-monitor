from nicegui import ui

class Layout:

    def __init__(self):
        with ui.header().classes('bg-blue-800 text-white items-center'):
            ui.label('EOM Dashboard').classes('text-xl')

            ui.space()

            ui.button('Dashboard', on_click=lambda: ui.navigate.to('/'))
            ui.button('View Device', on_click=lambda: ui.navigate.to('/view/device'))

        self.content = ui.column().classes('w-full p-4')