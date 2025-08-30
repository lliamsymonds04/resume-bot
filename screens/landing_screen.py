from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.layout import Layout, HSplit, Window
from prompt_toolkit.layout.controls import FormattedTextControl
from screens.screen_base import Screen

line_len = 70

ascii_art = r"""__________                                     __________        __   
\______   \ ____   ________ __  _____   ____   \______   \ _____/  |_ 
 |       _// __ \ /  ___/  |  \/     \_/ __ \   |    |  _//  _ \   __\
 |    |   \  ___/ \___ \|  |  /  Y Y  \  ___/   |    |   (  <_> )  |  
 |____|_  /\___  >____  >____/|__|_|  /\___  >  |______  /\____/|__|  
        \/     \/     \/            \/     \/          \/             """

class LandingScreen(Screen):
    def __init__(self):
        super().__init__("landing")
        self.control = FormattedTextControl(self.render, focusable=True)
        self.container = HSplit([Window(content=self.control, always_hide_cursor=True)])
        self.state = {"selection": 0}
        self.options = ["Config", "Find Jobs", "Something else idk"]

    def render(self):
        frags = []
        frags.append(("", ascii_art))
        frags.append(("", "\n" + "="*self.line_len + "\n"))
        frags.append(("", "Welcome to Resume Bot!\n\n"))
        frags.append(("", "Options:\n"))

        # render options
        rendered_options = self.render_options()
        frags.extend(rendered_options)

        controls = self.get_default_controls()
        frags.extend(controls)
        return frags

    def layout(self):
        return Layout(self.container)

    def keybindings(self, app_state=None):
        kb = KeyBindings()

        @kb.add("q")
        def _(event):
            event.app.exit()

        self.bind_move_options(kb)

        @kb.add("enter")
        def _(event):
            selected_option = self.options[self.state["selection"]]
            if selected_option == "Config":
                app_state.switch_screen("config")
            elif selected_option == "Find Jobs":
                app_state.switch_screen("find_jobs")
            else:
                pass

        return kb