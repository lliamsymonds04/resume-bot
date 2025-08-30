from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.layout import Layout, HSplit, Window
from prompt_toolkit.layout.controls import FormattedTextControl
from screens.screen_base import Screen



class ConfigScreen(Screen):
    def __init__(self):
        super().__init__("config")
        self.control = FormattedTextControl(self.render, focusable=True)
        self.container = HSplit([Window(content=self.control, always_hide_cursor=True)])

    def render(self):
        return [("", "Config Screen")]

    def layout(self):
        return Layout(self.container)
    
    def keybindings(self, app_state=None):
        kb = KeyBindings()

        @kb.add("q")
        def _(event):
            event.app.exit()

        @kb.add("b")
        def _(event):
            app_state.switch_screen("landing")

        return kb