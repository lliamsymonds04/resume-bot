from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.layout import Layout, HSplit, Window
from prompt_toolkit.layout.controls import FormattedTextControl
from screens.screen_base import Screen

ascii_art = r"""
_________                _____.__        
╲_   ___ ╲  ____   _____╱ ____╲__│ ____  
╱    ╲  ╲╱ ╱  _ ╲ ╱    ╲   __╲│  │╱ ___╲ 
╲     ╲___(  <_> )   │  ╲  │  │  ╱ ╱_╱  >
 ╲______  ╱╲____╱│___│  ╱__│  │__╲___  ╱ 
        ╲╱            ╲╱        ╱_____╱  
"""

options = ["Update skills", "Option 2", "Option 3"]
class ConfigScreen(Screen):
    def __init__(self):
        super().__init__("config")
        self.control = FormattedTextControl(self.render, focusable=True)
        self.container = HSplit([Window(content=self.control, always_hide_cursor=True)])
        self.state = {"selection": 0}
        self.options = ["Update skills", "Option 2", "Option 3"]

    def render(self):
        frags = []
        frags.append(("", ascii_art))
        frags.append(("", "\n" + "="*self.line_len + "\n"))
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
            app_state.switch_screen("landing")

        self.bind_move_options(kb)

        return kb