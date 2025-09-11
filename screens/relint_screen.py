import asyncio
import logging
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.layout import Layout, HSplit, Window
from prompt_toolkit.layout.controls import FormattedTextControl
from prompt_toolkit.widgets import TextArea, Label
from screens.screen_base import Screen
from fill_resume import save_resume
from make_cover_letter import save_cover_letter
from ai.resume_util import get_output_path, save_pdf, get_md_path

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
        
        self.job_input = TextArea(
            text="",
            height=1,
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
            Label(text="Use to update pdfs from markdown if self-edits were made.\n"),
            Label(text=""),  # Spacer
            self.job_input,
            Label(text=""),  # Spacer
            self.status_label,
            Label(text=""),  # Spacer
            Label(text="Press Enter to relint cv | Press Ctrl+C to clear | Press 'q' to go back"),
        ])
        
        # Combine header and form
        self.container = HSplit([
            header,
            Window(height=1),  # Separator
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

    def relint_resume(self, job_name):
        self.status_label.text = "Relinting resume..."
        self.redraw()

        output_path = get_output_path(job_name) 
        try:
            md_file_path = get_md_path(output_path["base_path"], job_name)
            save_pdf(md_file_path, output_path["base_path"], output_path["user_name"], "resume", [])
            self.status_label.text = "Resume relinted successfully!"
        except Exception as e:
            logging.error(f"Error relinting resume: {e}")
            self.status_label.text = f"Error relinting resume: {e}"
        self.redraw()

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
            asyncio.create_task(self.relint_resume())
            pass

        @kb.add("c-c")  # Ctrl+C
        def _(event):
            # Clear input
            self.clear_input()
            self.redraw()

        return kb

    def on_show(self):
        from prompt_toolkit.application import get_app
        get_app().layout.focus(self.job_input)