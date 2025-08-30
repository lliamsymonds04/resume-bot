from prompt_toolkit.application import Application
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.layout import Layout
from prompt_toolkit.widgets import TextArea, Box

LINE_LEN = 70
class Screen:
    def __init__(self, name):
        self.name = name
        self.line_len = LINE_LEN

    def layout(self):
        """Return the screen's layout"""
        return Layout(Box(TextArea(text=f"This is {self.name}")))

    def keybindings(self, app_state):
        """Return screen-specific keybindings"""
        kb = KeyBindings()
        return kb