from prompt_toolkit import Application
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
ascii_art += "\n" + "="*line_len + "\n"

options = ["Config", "Seek", "Something else idk"]

class LandingScreen(Screen):
    def __init__(self):
        super().__init__("landing")
        self.control = FormattedTextControl(self.render, focusable=True)
        self.container = HSplit([Window(content=self.control, always_hide_cursor=True)])
        self.state = {"selection": 0}

    def render(self):
        frags = []
        frags.append(("", ascii_art))
        frags.append(("", "Welcome to Resume Bot!\n\n"))
        frags.append(("", "Options:\n"))

        # render options
        for i, option in enumerate(options):
            prefix = "👉 " if i == self.state["selection"] else "   "
            style = "reverse" if i == self.state["selection"] else ""
            frags.append((style, f"{prefix}{option}\n"))

        frags.append(("", "\n" + "="*line_len))
        frags.append(("", "\n[j] down, [k] up, [enter] select, [q] quit.\n"))
        return frags

    def layout(self):
        return Layout(self.container)

    def keybindings(self, app_state=None):
        kb = KeyBindings()

        @kb.add("q")
        def _(event):
            event.app.exit()

        @kb.add("j")
        def _(event):
            self.state["selection"] = (self.state["selection"] + 1) % len(options)
            self.control.text = self.render()
            event.app.invalidate()

        @kb.add("k")
        def _(event):
            self.state["selection"] = (self.state["selection"] - 1) % len(options)
            self.control.text = self.render()
            event.app.invalidate()

        return kb