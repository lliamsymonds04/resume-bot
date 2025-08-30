from prompt_toolkit.application import Application
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.layout import Layout
from prompt_toolkit.widgets import TextArea, Box

class Screen:
    def __init__(self, name):
        self.name = name

    def layout(self):
        """Return the screen's layout"""
        return Layout(Box(TextArea(text=f"This is {self.name}")))

    def keybindings(self, app_state):
        """Return screen-specific keybindings"""
        kb = KeyBindings()
        return kb