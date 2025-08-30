from prompt_toolkit import Application
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.layout import Layout, HSplit, Window
from prompt_toolkit.layout.controls import FormattedTextControl

from screens.screen_base import Screen

ascii_art = r"""__________                                     __________        __   
\______   \ ____   ________ __  _____   ____   \______   \ _____/  |_ 
 |       _// __ \ /  ___/  |  \/     \_/ __ \   |    |  _//  _ \   __\
 |    |   \  ___/ \___ \|  |  /  Y Y  \  ___/   |    |   (  <_> )  |  
 |____|_  /\___  >____  >____/|__|_|  /\___  >  |______  /\____/|__|  
        \/     \/     \/            \/     \/          \/             """
ascii_art += "\n" + "="*70 + "\n"


class LandingScreen(Screen):
    def __init__(self):
        super().__init__("landing")
        self.control = FormattedTextControl(self.render, focusable=True)
        self.container = HSplit([Window(content=self.control, always_hide_cursor=True)])

    def render(self):
        frags = []
        frags.append(("", ascii_art))
        frags.append(("", "\nPress Q to quit.\n"))
        return frags

    def layout(self):
        return Layout(self.container)

    def keybindings(self, app_state=None):
        kb = KeyBindings()

        @kb.add("q")
        def _(event):
            event.app.exit()

        return kb