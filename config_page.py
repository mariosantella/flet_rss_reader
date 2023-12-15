import flet as ft

def config_page_view(page, navigation_bar):
    def save_rss_url(e):
        rss_url = rss_url_input.value
        page.client_storage.set("rss_url", rss_url)
        page.update()

    rss_url_input = ft.TextField(label="RSS Feed URL", width=300, value=page.client_storage.get("rss_url"))
    save_button = ft.TextButton(text="Save", on_click=save_rss_url)

    return ft.View(controls=[rss_url_input, save_button, navigation_bar])