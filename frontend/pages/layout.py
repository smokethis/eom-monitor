from nicegui import ui

class Layout:

    def __init__(self):
        with ui.header().classes('bg-blue-800 text-white items-center'):
            ui.label('EOM Dashboard').classes('text-xl')

            ui.space()

            ui.button('Dashboard', on_click=lambda: ui.navigate.to('/'))
            ui.button('Logs', on_click=lambda: ui.navigate.to('/logs'))
            ui.button('Settings', on_click=lambda: ui.navigate.to('/settings'))

        self.content = ui.column().classes('w-full p-4')