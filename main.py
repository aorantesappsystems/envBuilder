# main.py
import flet as ft
from pages.login import LoginPage  # Importamos desde la carpeta 'pages'

def main(page: ft.Page):
    def switch_page(new_page):
        try:
            page.controls.clear()
            page.controls.append(new_page)
            page.update()
        except Exception as e:
            print(f"Error switching page: {e}")  # Basic error handling

    # Inicia en la página de login
    switch_page(LoginPage(switch_page=switch_page, page=page))

ft.app(target=main)
