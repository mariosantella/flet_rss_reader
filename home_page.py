import flet as ft
import feedparser
from bs4 import BeautifulSoup
from datetime import datetime

def home_page_view(page, navigation_bar):
    rss_url = page.client_storage.get("rss_url")

    if not rss_url:
        return ft.View(controls=[ft.Text("Please set a valid RSS feed url in the configuration page", size=20), navigation_bar])

    feed = feedparser.parse(rss_url)

    posts_container = ft.Column(scroll=ft.ScrollMode.ALWAYS, expand=True)

    def highlight_link(e):
        e.control.style = ft.TextStyle(decoration=ft.TextDecoration.UNDERLINE, color=ft.colors.BLUE)

    def unhighlight_link(e):
        e.control.style = ft.TextStyle(decoration=ft.TextDecoration.NONE, color=ft.colors.BLACK)

    for entry in feed.entries:
        # Extract link
        post_link = entry.link

        # Extract title and truncate text
        title = entry.title[:70] + '...' if len(entry.title) > 70 else entry.title

        # Creating textspans for links
        title_span = ft.TextSpan(
            title,
            style=ft.TextStyle(size=20, weight="bold", decoration=ft.TextDecoration.UNDERLINE),
            url=post_link,
            on_enter=highlight_link,
            on_exit=unhighlight_link
        )

        # Date and author (if present)
        published_date = entry.get('published_parsed')
        if published_date:
            published_date = datetime(*published_date[:6]).strftime("%Y-%m-%d %H:%M:%S")
        else:
            published_date = "Data non disponibile"
        source = entry.get('source', {}).get('title', 'Fonte sconosciuta')

        source_date_text = ft.Text(f"Fonte: {source} - Data: {published_date}", size=12)

        soup = BeautifulSoup(entry.summary, 'html.parser')
        description_text = soup.get_text()

        # Img url
        image_url = None
        if 'media_content' in entry and entry.media_content:
            image_url = entry.media_content[0].get('url')

        image_control = ft.Image(src=image_url, fit=ft.ImageFit.FIT_WIDTH) if image_url else None


        # Post elements construction
        post_elements = [
            ft.Text(spans=[title_span]),
            source_date_text,
            image_control,
            ft.Text(description_text, size=12)
        ]

        post_container = ft.Container(
            content=ft.Column([element for element in post_elements if element], spacing=5),
            border=ft.border.all(1, ft.colors.GREY_200),
            padding=10
        )

        posts_container.controls.append(post_container)

    home_view = ft.View(controls=[posts_container, navigation_bar])
    return home_view
