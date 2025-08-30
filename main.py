from prompt_toolkit.application import Application
from screens.landing_screen import LandingScreen

class AppState:
    def __init__(self, app):
        self.app = app
        self.screens = {}
        self.current_screen = "main"

    def add_screen(self, screen):
        self.screens[screen.name] = screen

    def switch_screen(self, name):
        self.current_screen = name
        screen = self.screens[name]
        self.app.layout = screen.layout()
        self.app.key_bindings = screen.keybindings(self)
        self.app.invalidate()  # redraw the screen

# start app
app = Application(full_screen=True)
app_state = AppState(app)

landing_screen = LandingScreen()
app_state.add_screen(landing_screen)

# Make sure you're passing the **instance**, not the class
app_state.switch_screen("landing")
app.run()