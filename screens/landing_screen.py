from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.layout import Layout, HSplit, Window
from prompt_toolkit.widgets import Label
from prompt_toolkit.layout.controls import FormattedTextControl
from screens.screen_base import Screen

ascii_art = r"""__________                                     __________        __   
\______   \ ____   ________ __  _____   ____   \______   \ _____/  |_ 
 |       _// __ \ /  ___/  |  \/     \_/ __ \   |    |  _//  _ \   __\
 |    |   \  ___/ \___ \|  |  /  Y Y  \  ___/   |    |   (  <_> )  |  
 |____|_  /\___  >____  >____/|__|_|  /\___  >  |______  /\____/|__|  
        \/     \/     \/            \/     \/          \/             """

class LandingScreen(Screen):
    def __init__(self):
        super().__init__("landing")
        self.state = {"selection": 0}
        self.options = ["Find Jobs", "Manual Apply", "Config", "Relint"]

        self.control = FormattedTextControl(self.render, focusable=True)
        self.footer = FormattedTextControl(self.get_default_controls)

        self.create_layout()

    def render(self):
        frags = []
        frags.append(("", "Options:\n"))

        # render options
        rendered_options = self.render_options()
        frags.extend(rendered_options)

        return frags

    def create_layout(self):
        art_height = len(ascii_art.splitlines())
        header = HSplit([
            Window(content=FormattedTextControl(ascii_art), height=art_height + 1, always_hide_cursor=True),
            Window(height=1, char="=", style="class:line"),
            Label(text="Welcome to Resume Bot!\n"),
        ])
        
        # Input form (use a Window for the dynamic main content)
        form_content = HSplit([
            Window(content=self.control, always_hide_cursor=True, height=len(self.options) + 2),
            Window(height=1, char="-", style="class:line"),
            Label(text=self.get_default_controls()),
        ])
        
        # Combine header and form
        self.container = HSplit([
            header,
            form_content
        ])

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
            elif selected_option == "Manual Apply":
                app_state.switch_screen("manual_apply")
            elif selected_option == "Relint":
                app_state.switch_screen("relint")
            else:
                pass

        return kb