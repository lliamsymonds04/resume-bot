import asyncio
from asyncio import subprocess
import os
from platform import platform
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.layout import Layout, HSplit, Window
from prompt_toolkit.layout.controls import FormattedTextControl
from prompt_toolkit.widgets import Label, TextArea
from ai.resume_util import get_input_data, get_output_path, open_job_output_folder
from make_cover_letter import make_cover_letter, save_cover_letter
from make_resume import save_resume, make_resume
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
                self.status_label,
                Label(text=""),
                Window(height=1, char="-", style="class:line"),
                Label(text="Press 'q' to go back to job listings"),
            ])
        else:
            form_content = HSplit([
                Label(text="Type additional notes for the AI here"),
                self.notes_input,
                Label(text=""),
                self.status_label,
                Label(text=""),
                Window(height=1, char="-", style="class:line"),
                Label(text="Enter | [q] to go back | [Ctrl+O] to open output folder"),
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

    def clear_input(self):
        self.status_label.text = ""
        self.notes_input.text = ""
        self.note_given = False

    async def process_application(self, job_description: JobDescription, notes: str):
        self.add_line_to_status("Processing application...")

        self.add_line_to_status(f"• Tailoring skills...")

        input_data = await get_input_data(job_description)
        input_data["additional_notes"] = notes

        self.add_line_to_status(f"✓ Skills tailored successfully")
        self.add_line_to_status(f"• Generating resume...")
        
        resume = await make_resume(input_data)
        save_resume(resume, job_description.company, keep_md=True)
        
        self.add_line_to_status(f"✓ Successfully generated resume")
        self.add_line_to_status(f"• Generating cover letter...")

        cover_letter = await make_cover_letter(input_data)
        save_cover_letter(cover_letter, job_description.company, keep_md=True)
        
        self.add_line_to_status(f"✓ Successfully generated cover letter")
        self.add_line_to_status(f"✓ All done! Check the output folder for your files.")

    def keybindings(self, app_state=None):
        kb = KeyBindings()

        @kb.add("q")
        def _(event):
            self.clear_input()
            app_state.switch_screen("find_jobs")

        @kb.add("enter")
        def _(event):
            if self.note_given:
                # Already given note, do nothing
                return

            notes = self.notes_input.text.strip()
            self.note_given = True

            asyncio.create_task(self.process_application(self.job_description, notes))

        kb.add("c-o")
        def _(event):
            open_job_output_folder(self.job_description.company)
            

        return kb

    def on_show(self, job_description: JobDescription):
        self.clear_input()
        self.job_description = job_description
        app = get_app()
        app.layout.focus(self.notes_input)