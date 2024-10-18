import flet as ft
from extra.colors import ThemeColors  

class MainPage(ft.Container):
    def __init__(self, switch_page):
        super().__init__()
        self.switch_page = switch_page
        self.expand = True
        
        
        # Use colors from ThemeColors class
        self.color_primary = ThemeColors.PRIMARY
        self.color_surface = ThemeColors.SURFACE
        
        # Barra de navegación
        self.navigation = ft.Container(
            content=ft.Column(
                controls=[
                    self.create_user_info(),
                    self.create_navigation_buttons(),
                ],
                alignment=ft.MainAxisAlignment.START,
                spacing=10,
            ),
            width=250,
            bgcolor=self.color_surface['a10'],
            padding=20,
            margin=20,
            border_radius=10,
        )

        # Contenido principal
        self.main_content = ft.Container(
            content=ft.Text("¡Bienvenido a la página principal!", size=24),
            expand=True,
            padding=20,
        )

        # Estructura principal
        self.content = ft.Row(
            controls=[
                self.navigation,
                self.main_content,
            ],
            expand=True,
        )

    def create_user_info(self):
        # Aquí puedes agregar tu avatar, nombre y correo electrónico
        # user have an avatar, name and email 
        self.avatar = ft.Image(src="", width=100, height=100, border_radius=50)
        self.name_label = ft.Text("Tu Nombre", size=18)
        self.email_label = ft.Text("tu_correo@ejemplo.com", size=14)

        return ft.Column(
            controls=[
                self.avatar,
                self.name_label,
                self.email_label,
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=5,
        )

    def create_navigation_buttons(self):
        # Opciones de navegación
        self.button1 = ft.TextButton("Opción 1", on_click=self.change_content)
        self.button2 = ft.TextButton("Opción 2", on_click=self.change_content)
        self.button3 = ft.TextButton("Opción 3", on_click=self.change_content)

        return ft.Column(
            controls=[
                self.button1,
                self.button2,
                self.button3,
            ],
            alignment=ft.MainAxisAlignment.START,
            spacing=10,
        )

    def change_content(self, e):
        # Cambia el contenido principal según el botón presionado
        if e.control.text == "Opción 1":
            self.main_content.content = ft.Text("Contenido de la Opción 1", size=24)
        elif e.control.text == "Opción 2":
            self.main_content.content = ft.Text("Contenido de la Opción 2", size=24)
        elif e.control.text == "Opción 3":
            self.main_content.content = ft.Text("Contenido de la Opción 3", size=24)

        self.main_content.update()  # Actualiza el contenido
