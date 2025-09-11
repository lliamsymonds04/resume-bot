from prompt_toolkit.application import Application
from screens.find_jobs_screen import FindJobsScreen
from screens.landing_screen import LandingScreen
from screens.config_screen import ConfigScreen
from screens.manual_apply import ManualApplyScreen
from screens.relint_screen import RelintScreen
from services.job_database import JobDatabase

class AppState:
    def __init__(self, app, db):
        self.app = app
        self.db = db
        self.screens = {}
        self.current_screen = "main"

    def add_screen(self, screen):
        self.screens[screen.name] = screen
        screen.db = self.db  # Provide db instance to screen

    def switch_screen(self, name):
        self.current_screen = name
        screen = self.screens[name]
        self.app.layout = screen.layout()
        self.app.key_bindings = screen.keybindings(self)
        self.app.invalidate()  # redraw the screen
        if hasattr(screen, "on_show"):
            screen.on_show()

# initialize database
db = JobDatabase()
db.clear_old_jobs() 

# start app
app = Application(full_screen=True)
app_state = AppState(app, db)

# screens
landing_screen = LandingScreen()
config_screen = ConfigScreen()
find_jobs_screen = FindJobsScreen()
manual_apply_screen = ManualApplyScreen()
relint_screen = RelintScreen() 

# add screens
app_state.add_screen(landing_screen)
app_state.add_screen(config_screen)
app_state.add_screen(find_jobs_screen)
app_state.add_screen(manual_apply_screen)
app_state.add_screen(relint_screen)

# init
app_state.switch_screen("landing")
app.run()