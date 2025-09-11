import asyncio
import logging
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.layout import Layout, HSplit, Window
from prompt_toolkit.layout.controls import FormattedTextControl
from prompt_toolkit.widgets import TextArea, Label
from screens.screen_base import Screen
from fill_resume import save_resume
from make_cover_letter import save_cover_letter

ascii_art = r"""
__________       .__  .__        __   
\______   \ ____ |  | |__| _____/  |_ 
 |       _// __ \|  | |  |/    \   __\
 |    |   \  ___/|  |_|  |   |  \  |  
 |____|_  /\___  >____/__|___|  /__|  
        \/     \/             \/     
"""

class RelintScreen(Screen):
    def __init__(self):
        super().__init__("relint")
        self.line_len = 75
        
        # Create URL input field
        self.url_input = TextArea(
            text="",
            height=2,
            multiline=True,
            scrollbar=False,
            wrap_lines=True
        )
        
        # Status display
        self.status_label = Label(text="")
        
        # Create the layout
        self.create_layout()

    def create_layout(self):
        # Header
        header = Window(
            content=FormattedTextControl(self.render_header),
            height=10,
            always_hide_cursor=True
        )
        
        # Input form
        form_content = HSplit([
            Label(text=""),  # Spacer
            self.url_input,
            Label(text=""),  # Spacer
            self.status_label,
            Label(text=""),  # Spacer
            Label(text="Press Enter to relint cv | Press Ctrl+C to clear | Press 'q' to go back"),
        ])
        
        # Combine header and form
        self.container = HSplit([
            header,
            form_content
        ])

    def render_header(self):
        frags = []
        frags.append(("", ascii_art))
        frags.append(("", "\n" + "="*self.line_len + "\n"))
        frags.append(("", "Enter name of job:\n"))
        return frags

    def layout(self):
        return Layout(self.container)

    def clear_input(self):
        self.url_input.text = ""
        self.status_label.text = ""

    def keybindings(self, app_state=None):
        kb = KeyBindings()

        @kb.add("q")
        def _(event):
            app_state.switch_screen("landing")

        @kb.add("enter")
        def _(event):
            # asyncio.create_task(self.process_job())
            pass

        @kb.add("c-c")  # Ctrl+C
        def _(event):
            # Clear input
            self.clear_input()
            self.redraw()

        return kb