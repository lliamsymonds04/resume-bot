from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.layout import Layout, HSplit, Window
from prompt_toolkit.layout.controls import FormattedTextControl
from prompt_toolkit.widgets import Label, TextArea
from screens.screen_base import Screen
from models.job_description import JobDescription
from prompt_toolkit.application import get_app

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

        # Status display
        self.status_label = Label(text="")
        self.notes_input = TextArea(
            text="",
            height=5,
            multiline=True,
            wrap_lines=True
        ) 

        self.note_given = False
        
        # Create the layout
        self.create_layout()

    def create_layout(self):
        # Header
        art_height = len(ascii_art.splitlines())
        header = HSplit([
            Window(content=FormattedTextControl(ascii_art), height=art_height, always_hide_cursor=True),
            Window(height=1, char="=", style="class:line"),
        ])

        if self.note_given:
            form_content = HSplit([
                Window(height=1, char="=", style="class:line"),
                self.status_label,
                Label(text=""),
                Window(height=1, char="-", style="class:line"),
                Label(text="Press 'q' to go back to job listings"),
            ])
        else:
            form_content = HSplit([
                Window(height=1, char="=", style="class:line"),
                Label(text="Type additional notes for the AI here"),
                self.notes_input,
                Label(text=""),
                self.status_label,
                Label(text=""),
                Window(height=1, char="-", style="class:line"),
                Label(text="Enter | Press 'q' to go back to job listings"),
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
        self.notes_input.text = ""
        self.note_given = False

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
        self.clear_input()
        self.job_description = job_description
        app = get_app()
        app.layout.focus(self.notes_input)