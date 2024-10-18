import flet as ft

class MainPage(ft.Container):
    def __init__(self):
        super().__init__()
        self.expand = True
        self.bgcolor = "#f0f0f0"  # Set a light background color
        self.padding = 20  # Add some padding

        self.content = ft.Column(
            controls=[
                ft.Text(value="¡Bienvenido a la página principal!", size=30, color="black"),
                ft.Container(height=20),  # Space between elements
                ft.Row(
                    controls=[
                        ft.ElevatedButton(text="Ir a Configuración", on_click=self.go_to_settings),
                        ft.ElevatedButton(text="Cerrar sesión", on_click=self.logout),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,  # Center the buttons
                ),
            ],
            alignment=ft.MainAxisAlignment.CENTER,  # Center the text
        )

    def go_to_settings(self, e):
        # Implement navigation to the settings page here
        pass

    def logout(self, e):
        # Implement logout functionality here
        pass
