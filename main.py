import flet as ft
from home_page import home_page_view
from config_page import config_page_view

def main(page: ft.Page):
    page.window_width = 420
    page.window_height = 720
    page.title = "RSS flet reader"

    # NavigationBar Definition
    def create_navigation_bar(selected_index):
        return ft.NavigationBar(
            destinations=[
                ft.NavigationDestination(icon=ft.icons.HOME, label="Home"),
                ft.NavigationDestination(icon=ft.icons.SETTINGS, label="Configurazioni")
            ],
            on_change=lambda e: update_view(e.control.selected_index),
            selected_index=selected_index
        )

    # Update views (index based)
    def update_view(selected_index):
        navigation_bar = create_navigation_bar(selected_index)
        page.views.clear()
        if selected_index == 0:
            page.views.append(home_page_view(page, navigation_bar))
        elif selected_index == 1:
            page.views.append(config_page_view(page, navigation_bar))
        page.update()

    # First view to serve (int)
    update_view(0)

ft.app(target=main)