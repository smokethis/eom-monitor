from nicegui import ui

class PageHeader():
    def __init__(self, label):
        with ui.header():
            ui.label(label).classes('text-xl font-bold')
            ui.space()
            ui.button('Dashboard', on_click=lambda: ui.navigate.to('/'))
            ui.button('Edging', on_click=lambda: ui.navigate.to('/edging'))
            ui.button('View Device', on_click=lambda: ui.navigate.to('/view/device'))     
