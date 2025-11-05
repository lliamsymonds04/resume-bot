from prompt_toolkit.application import Application
from screens.find_jobs_screen import FindJobsScreen
from screens.job_description_screen import JobDescriptionScreen
from screens.landing_screen import LandingScreen
from screens.config_screen import ConfigScreen
from screens.manual_apply import ManualApplyScreen
from screens.relint_screen import RelintScreen
from screens.apply_screen import ApplyScreen
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

    def switch_screen(self, name, **kwargs):
        self.current_screen = name
        screen = self.screens[name]
        self.app.layout = screen.layout()
        self.app.key_bindings = screen.keybindings(self)
        self.app.invalidate()  # redraw the screen
        if hasattr(screen, "on_show"):
            screen.on_show(**kwargs)


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
job_description_screen = JobDescriptionScreen()
apply_screen = ApplyScreen()

# add screens
screens = [
    landing_screen,
    config_screen,
    find_jobs_screen,
    manual_apply_screen,
    relint_screen,
    job_description_screen,
    apply_screen,
]
for screen in screens:
    app_state.add_screen(screen)

# init
app_state.switch_screen("landing")
app.run()

