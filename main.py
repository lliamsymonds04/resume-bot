from prompt_toolkit.application import Application
from screens.find_jobs_screen import FindJobsScreen
from screens.landing_screen import LandingScreen
from screens.config_screen import ConfigScreen

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

# screens
landing_screen = LandingScreen()
config_screen = ConfigScreen()
find_jobs_screen = FindJobsScreen()

# add screens
app_state.add_screen(landing_screen)
app_state.add_screen(config_screen)
app_state.add_screen(find_jobs_screen)

# init
app_state.switch_screen("landing")
app.run()