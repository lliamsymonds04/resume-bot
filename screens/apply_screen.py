from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.layout import Layout, HSplit, Window
from prompt_toolkit.layout.controls import FormattedTextControl
from prompt_toolkit.widgets import Label
from screens.screen_base import Screen
from models.job_description import JobDescription

ascii_art = r"""
   _____                .__         .__                
  /  _  \ ______ ______ |  | ___.__.|__| ____    ____  
 /  /_\  \\____ \\____ \|  |<   |  ||  |/    \  / ___\ 
/    |    \  |_> >  |_> >  |_\___  ||  |   |  \/ /_/  >
\____|__  /   __/|   __/|____/ ____||__|___|  /\___  / 
        \/|__|   |__|        \/             \//_____/  
"""

class ApplyScreen(Screen):
    def __init__(self):
        super().__init__("apply")
        self.loaded = False
        
        # Status display
        self.status_label = Label(text="")
        
        # Create the layout
        self.create_layout()

    def create_layout(self):
        # Header
        header = Window(
            content=FormattedTextControl(ascii_art),
            height=8,
            always_hide_cursor=True
        )
        
        # Input form
        form_content = HSplit([
            Window(height=1, char="=", style="class:line"),
            self.status_label,
            Label(text=""),
            Window(height=1, char="-", style="class:line"),
        ])
        
        # Combine header and form
        self.container = HSplit([
            header,
            form_content
        ])

    def render_header(self):
        frags = []
        frags.append(("", ascii_art))
        return frags

    def layout(self):
        return Layout(self.container)

    def add_line_to_status(self, line):
        """Add a line to the status label"""
        if self.status_label.text:
            self.status_label.text += "\n"
        self.status_label.text += line
        self.redraw()

    def clear_input(self):
        self.status_label.text = ""

    def keybindings(self, app_state=None):
        kb = KeyBindings()

        @kb.add("q")
        def _(event):
            self.clear_input()
            app_state.switch_screen("find_jobs")

        @kb.add("enter")
        def _(event):
            pass

        return kb

    def on_show(self, job_description: JobDescription):
        pass