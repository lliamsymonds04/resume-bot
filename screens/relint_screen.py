import os
import logging
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.layout import Layout, HSplit, Window
from prompt_toolkit.layout.controls import FormattedTextControl
from prompt_toolkit.widgets import TextArea, Label
from screens.screen_base import Screen
from make_resume import get_resume_format_args
from make_cover_letter import get_cover_letter_format_args
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
            multiline=False,
            scrollbar=False,
            wrap_lines=True
        )
        
        # Status display
        self.status_label = Label(text="")
        
        # Create the layout
        self.create_layout()

    def create_layout(self):
        # Header
        art_height = len(ascii_art.splitlines())
        header = HSplit([
            Window(content=FormattedTextControl(ascii_art), height=art_height, always_hide_cursor=True),
            Window(height=1, char="=", style="class:line"),
        ])
        
        # Input form
        form_content = HSplit([
            Label(text="Enter name of job:"),
            self.job_input,
            Label(text=""),  # Spacer
            self.status_label,
            Label(text=""),  # Spacer
            Window(height=1, char="-", style="class:line"),
            Label(text="Press Enter to relint folder | Press Ctrl+C to clear | Press 'q' to go back"),
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
        frags.append(("", "Use to update pdfs from markdown if self-edits were made.\n"))
        return frags

    def layout(self):
        return Layout(self.container)

    def relint(self, job_name):
        job_name = job_name.strip().lower().replace(" ", "-")

        output_path = get_output_path(job_name) 

        # First try to relint the resume
        relint_success = False
        try:
            self.add_line_to_status("• Relinting resume...")
            tail_name = "resume"
            md_file_path = get_md_path(output_path["base_path"], tail_name)
            #check the markdown exists
            if not os.path.exists(md_file_path):
                raise FileNotFoundError(f"Markdown file not found: {md_file_path}")
            save_pdf(md_file_path, output_path["base_path"], output_path["user_name"], tail_name, get_resume_format_args())
            self.add_line_to_status("✓ Resume relinted successfully!\n")
            relint_success = True
        except Exception as e:
            logging.error(f"Error relinting resume: {e}")
            self.add_line_to_status(f"Error relinting resume: {e}\n")
            self.redraw()

        if not relint_success:
            return

        # Then try to relint the cover letter
        try:
            self.add_line_to_status("• Relinting cover letter...")
            tail_name = "cover-letter"
            md_file_path = get_md_path(output_path["base_path"], tail_name)
            save_pdf(md_file_path, output_path["base_path"], output_path["user_name"], tail_name, get_cover_letter_format_args())
            self.add_line_to_status("✓ Cover letter relinted successfully!\n")
        except Exception as e:
            logging.error(f"Error relinting cover letter: {e}")
            self.add_line_to_status(f"Error relinting cover letter: {e}\n")

        self.add_line_to_status(f"✓ All done! Check the output folder for your files.")

    def clear_input(self):
        self.job_input.text = ""
        self.status_label.text = ""

    def keybindings(self, app_state=None):
        kb = KeyBindings()

        @kb.add("q")
        def _(event):
            self.clear_input()
            app_state.switch_screen("landing")

        @kb.add("enter")
        def _(event):
            # get the job name from the input
            job_name = self.job_input.text.strip()
            if not job_name:
                self.status_label.text = "Please enter a job name"
                self.redraw()
                return

            self.relint(job_name)
            pass

        @kb.add("c-c")  # Ctrl+C
        def _(event):
            # Clear input
            self.clear_input()
            self.redraw()

        return kb

    def on_show(self):
        from prompt_toolkit.application import get_app
        self.clear_input()
        get_app().layout.focus(self.job_input)