import flet as ft
from github import Github, Auth, BadCredentialsException
from .main_page import MainPage
from extra.colors import ThemeColors  

class LoginPage(ft.Container):
    def __init__(self, switch_page, page):
        super().__init__()
        self.page = page
        self.switch_page = switch_page
        self.expand = True
        self.error_message = None

        # Use colors from ThemeColors class
        self.color_primary = ThemeColors.PRIMARY
        self.color_surface = ThemeColors.SURFACE
        
        self.page.title = 'Login'
        self.page.bgcolor = self.color_surface['a0']

        # Create the background image as a container
        background_image = ft.Image(src="assets/some.gif", fit=ft.ImageFit.COVER)

        # Main layout
        self.content = ft.Stack(
            controls=[
                ft.Container(
                    content=background_image,
                    width=self.page.width,
                    height=self.page.height,
                    alignment=ft.alignment.center,
                ),
                ft.Column(
                    controls=[
                        self.create_user_info(),
                        self.create_login_switcher()
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    height=self.page.height,
                ),
            ],
            alignment=ft.alignment.center,
        )

        # Load token from local storage
        self.load_token()

        # Track the current card
        self.current_card = 'token'  # 'token' or 'credentials'

    def create_user_info(self):
        # Define labels and image for user information
        self.user_name_label = ft.Text("", size=20, color=self.color_primary['a0'])
        self.user_login_label = ft.Text("", size=16, color=self.color_primary['a0'])
        self.user_email_label = ft.Text("", size=16, color=self.color_primary['a0'])
        self.user_profile_image = ft.Container(
            content=ft.Image(src="", fit=ft.ImageFit.COVER, width=100, height=100),
            width=100,
            height=100,
            border_radius=50,
            alignment=ft.alignment.center,
            bgcolor=self.color_surface['a30'],  # Placeholder background
        )

        return ft.Row(
            controls=[
                self.user_profile_image,
                ft.Column(
                    controls=[
                        self.user_name_label,
                        self.user_login_label,
                        self.user_email_label,
                    ],
                    alignment=ft.MainAxisAlignment.START,
                    horizontal_alignment=ft.CrossAxisAlignment.START,
                    spacing=5,
                ),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=20,
        )

    def create_login_switcher(self):
        self.token_card = self.create_token_card()
        self.credentials_card = self.create_credentials_card()

        self.switcher = ft.AnimatedSwitcher(
            self.token_card,
            transition=ft.AnimatedSwitcherTransition.SCALE,
            duration=500,
            reverse_duration=500,
            switch_in_curve=ft.AnimationCurve.BOUNCE_OUT,
            switch_out_curve=ft.AnimationCurve.BOUNCE_IN,
        )

        self.switch_button = ft.TextButton(
            "Iniciar con credenciales", 
            on_click=self.switch_cards
        )

        return ft.Column(
            controls=[
                self.switcher,
                self.switch_button,
            ],
            alignment=ft.alignment.center,
        )

    def create_token_card(self):
        self.pwd_input = ft.TextField(
            password=True,
            hint_text='Github Token',
            cursor_color=self.color_primary['a10'],
            bgcolor=self.color_surface['a20'],  
            border_color=self.color_surface['a30'],
            focused_bgcolor=self.color_surface['a30'],
            focused_border_width=2,
            focused_border_color=self.color_primary['a10'],
            filled=True,
            border_radius=7,
            height=60,
            on_change=self.on_token_change
        )

        # Create token card layout
        return ft.Container(
            bgcolor=self.color_surface['a10'],
            border_radius=20,
            padding=30,
            margin=20,
            content=ft.Column(
                controls=[
                    self.pwd_input,
                    ft.Container(
                        data='login_clicked',
                        on_click=self.validate_github_token,
                        height=50,
                        bgcolor=self.color_primary['a0'],
                        border_radius=20,
                        alignment=ft.alignment.center,
                        content=ft.Text(value='Continue', font_family='Poppins Medium', size=16, color=self.color_surface['a0'])
                    ),
                ]
            ),
            height=300,
            width=500,
            alignment=ft.alignment.center,
        )

    def create_credentials_card(self):
        # Create input fields for username and password
        self.username_input = ft.TextField(hint_text='Username', border_radius=7, height=60)
        self.password_input = ft.TextField(password=True, hint_text='Password', border_radius=7, height=60)

        # Create credentials card layout
        return ft.Container(
            bgcolor=self.color_surface['a10'],
            border_radius=20,
            padding=30,
            margin=20,
            content=ft.Column(
                controls=[
                    self.username_input,
                    self.password_input,
                    ft.Container(
                        data='login_clicked',
                        on_click=self.validate_credentials,
                        height=50,
                        bgcolor=self.color_primary['a0'],
                        border_radius=20,
                        alignment=ft.alignment.center,
                        content=ft.Text(value='Log In', font_family='Poppins Medium', size=16, color=self.color_surface['a0'])
                    ),
                ]
            ),
            height=300,
            width=500,
            alignment=ft.alignment.center,
        )

    def switch_cards(self, e):
        if self.current_card == 'token':
            self.switcher.content = self.credentials_card
            self.switch_button.text = "Iniciar con token"  # Change button text
            self.current_card = 'credentials'
        else:
            self.switcher.content = self.token_card
            self.switch_button.text = "Iniciar con credenciales"  # Change button text
            self.current_card = 'token'

        self.switcher.update()
        self.switch_button.update()

    def load_token(self):
        self.token = self.page.client_storage.get('token')
        if self.token:
            self.update_user_info(self.token)
            self.pwd_input.value = self.token
        
        # Load credentials if available
        self.username = self.page.client_storage.get('username')
        self.password = self.page.client_storage.get('password')
        if self.username and self.password:
            self.username_input.value = self.username
            self.password_input.value = self.password

    def on_token_change(self, e):
        token = self.pwd_input.value
        if token:
            self.update_user_info(token)

    def update_user_info(self, token):
        try:
            auth = Auth.Token(token)
            g = Github(auth=auth)
            user = g.get_user()
            self.user_name_label.value = user.name if user.name else "Nombre no disponible"
            self.user_login_label.value = user.login if user.login else "Nombre de usuario no disponible"
            self.user_email_label.value = user.email if user.email else "Email no disponible"

            self.user_profile_image.content = ft.Image(src=user.avatar_url, fit=ft.ImageFit.COVER)

            self.user_name_label.update()
            self.user_login_label.update()
            self.user_email_label.update()
            self.user_profile_image.update()
            g.close()
        except Exception:
            pass

    def validate_github_token(self, e):
        token = self.pwd_input.value
        try:
            auth = Auth.Token(token)
            g = Github(auth=auth)
            repos = g.get_user().get_repos()

            if repos.totalCount == 0:
                self.show_error("No tienes repositorios asociados con este token.")
            else:
                self.page.client_storage.set('token', token)
                self.switch_page(MainPage(self.switch_page))
            g.close()
        except Exception:
            self.show_error("El token no es válido. Por favor, intenta de nuevo.")

    def show_error(self, message):
        if self.error_message:
            self.error_container.controls.clear()

        self.error_container.controls.append(ft.Text(value=message, color=ft.colors.RED))
        self.pwd_input.bgcolor = ft.colors.RED_600
        self.update()

    def validate_credentials(self, e):
        username = self.username_input.value
        password = self.password_input.value

        try:
            g = Github(username, password)  # Authenticate with the provided username and password
            user = g.get_user()  # Try to fetch the authenticated user to validate credentials
            
            # If successful, proceed with your logic (like navigating to the main page)
            self.page.client_storage.set('username', username)  # Store username if needed
            self.page.client_storage.set('password', password)  # Store password if needed
            self.switch_page(MainPage(self.switch_page))
            return True  # Credentials are valid
        except BadCredentialsException:
            self.show_error("Credenciales inválidas. Por favor, intenta de nuevo.")
            return False  # Invalid credentials
        except Exception as e:
            self.show_error(f"An error occurred: {e}")
            return False  # Handle other exceptions if needed

