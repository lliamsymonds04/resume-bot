import asyncio
import logging
import textwrap
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.layout import Layout, HSplit, Window
from prompt_toolkit.layout.controls import FormattedTextControl
from screens.screen_base import Screen

ascii_art = r"""
   _____                             .__       _____             .___      
  /     \ _____    ____  __ _______  |  |     /     \   ____   __| _/____  
 /  \ /  \\__  \  /    \|  |  \__  \ |  |    /  \ /  \ /  _ \ / __ |/ __ \ 
/    Y    \/ __ \|   |  \  |  // __ \|  |__ /    Y    (  <_> ) /_/ \  ___/ 
\____|__  (____  /___|  /____/(____  /____/ \____|__  /\____/\____ |\___  >
        \/     \/     \/           \/               \/            \/    \/ 
"""

class ManualApplyScreen(Screen):
    def __init__(self):
        super().__init__("manual_apply")
        self.control = FormattedTextControl(self.render, focusable=True)
        self.container = HSplit([Window(content=self.control, always_hide_cursor=True)])
        self.line_len = 75

    def render(self):
        frags = []
        frags.append(("", ascii_art))
        frags.append(("", "\n" + "="*self.line_len + "\n"))

        return frags

    def layout(self):
        return Layout(self.container)

    def keybindings(self, app_state=None):
        kb = KeyBindings()

        @kb.add("q")
        def _(event):
            app_state.switch_screen("landing")

        return kb
