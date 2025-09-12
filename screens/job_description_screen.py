import logging
import asyncio
from time import sleep
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.layout import Layout, HSplit, Window
from prompt_toolkit.layout.controls import FormattedTextControl
from prompt_toolkit.widgets import Label
from screens.screen_base import Screen
from models.job_listing import JobListing
from job_scraping import scrape_job_description
from ai.parse_job import parse_job_description

ascii_art = r"""
     ____.     ___.     ________                             .__        __  .__               
    |    | ____\_ |__   \______ \   ____   ______ ___________|__|______/  |_|__| ____   ____  
    |    |/  _ \| __ \   |    |  \_/ __ \ /  ___// ___\_  __ \  \____ \   __\  |/  _ \ /    \ 
/\__|    (  <_> ) \_\ \  |    `   \  ___/ \___ \\  \___|  | \/  |  |_> >  | |  (  <_> )   |  \
\________|\____/|___  / /_______  /\___  >____  >\___  >__|  |__|   __/|__| |__|\____/|___|  /
                    \/          \/     \/     \/     \/         |__|                       \/ 
"""

class JobDescriptionScreen(Screen):
    def __init__(self):
        super().__init__("job_description")
        self.loaded = False
        
        # Status display
        self.status_label = Label(text="")
        
        # Create the layout
        self.create_layout()

    def create_layout(self):
        art_height = len(ascii_art.splitlines())
        header = HSplit([
            Window(content=FormattedTextControl(ascii_art), height=art_height, always_hide_cursor=True),
            Window(height=1, char="=", style="class:line"),
        ])
        
        # Input form
        form_content = HSplit([
            self.status_label,
            Label(text=""),
            Window(height=1, char="-", style="class:line"),
            Label(text=self.get_controls_text()),
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

    def get_controls_text(self):
        if self.loaded:
            return "Press [enter] to apply | [q] to go back."
        else:
            return "Press [q] to go back."

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
            if not self.loaded:
                return
            app_state.switch_screen("apply", job_description=self.job_description)

        return kb
    
    async def load_job(self, job: JobListing):
        self.add_line_to_status(f"Loading Job Description for {job.title}...")
        self.add_line_to_status("• Scraping job link...")

        # Scrape job link to get full description
        try:
            with self.suppress_output():
                raw_job_description = await scrape_job_description(job.link)
        except Exception as e:
            logging.error(f"Error scraping job info for {job.link}", exc_info=True)
            self.add_line_to_status("Error retrieving job description.")
            return

        if not raw_job_description:
            return
        
        # Parse job info
        self.add_line_to_status("• Parsing job description...")
        job_description = parse_job_description(raw_job_description)
        self.add_line_to_status("✓ Job description loaded successfully!\n")
        self.redraw()
        
        self.loaded = True
        self.status_label.text = ""  # clear status
        self.add_line_to_status(f"Job Title: {job.title}")
        self.add_line_to_status(f"Company: {job.company}")
        self.add_line_to_status(f"Location: {job.location}")
        if job_description.salary:
            self.add_line_to_status(f"Salary: {job_description.salary}")

        if len(job_description.responsibilities) > 0:
            self.add_line_to_status("Responsibilities:")
            responsibilities = " | ".join(job_description.responsibilities)
            self.add_line_to_status(f" - {responsibilities}")

        if len(job_description.requirements) > 0:
            self.add_line_to_status("Requirements:")
            requirements = " | ".join(job_description.requirements)
            self.add_line_to_status(f" - {requirements}")
            
        if len(job_description.skills) > 0 and len(job_description.responsibilities) == 0:
            self.add_line_to_status("Skills:")
            skills = " | ".join(job_description.skills)
            self.add_line_to_status(f" - {skills}")

        # set the job description self reference
        self.job_description = job_description


    def on_show(self, job: JobListing):
        if job is not None:
            self.loaded = False
            self.status_label.text = ""
            asyncio.create_task(self.load_job(job)) 