from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.layout import Layout, HSplit, Window
from prompt_toolkit.layout.controls import FormattedTextControl
from prompt_toolkit.widgets import Label
from screens.screen_base import Screen

ascii_art = r"""_________                _____.__        
╲_   ___ ╲  ____   _____╱ ____╲__│ ____  
╱    ╲  ╲╱ ╱  _ ╲ ╱    ╲   __╲│  │╱ ___╲ 
╲     ╲___(  <_> )   │  ╲  │  │  ╱ ╱_╱  >
 ╲______  ╱╲____╱│___│  ╱__│  │__╲___  ╱ 
        ╲╱            ╲╱        ╱_____╱  
"""

class ConfigScreen(Screen):
    def __init__(self):
        super().__init__("config")

        self.state = {"selection": 0}
        self.options = ["Update skills", "Option 2", "Option 3"]

        self.control = FormattedTextControl(self.render_options(), focusable=True)
        self.footer = FormattedTextControl(self.get_default_controls)

        self.create_layout()

    def create_layout(self):
        art_height = len(ascii_art.splitlines())
        header = HSplit([
            Window(content=FormattedTextControl(ascii_art), height=art_height, always_hide_cursor=True),
            Window(height=1, char="=", style="class:line"),
        ])
        
        # Input form (use a Window for the dynamic main content)
        form_content = HSplit([
            Label(text="Options:"),
            Window(content=self.control, always_hide_cursor=True, height=len(self.options) + 1),
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
            app_state.switch_screen("landing")

        self.bind_move_options(kb)

        return kb