import logging
import asyncio
from time import sleep
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.layout import Layout, HSplit, Window
from prompt_toolkit.layout.controls import FormattedTextControl
from prompt_toolkit.widgets import Label
from screens.screen_base import Screen
from models.job_listing import JobListing
from scraping.scrape_job_info import scrape_job_info
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
        self.line_len = 75
        
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
            self.status_label,
            Label(text=""),  # Spacer
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
    
    async def load_job(self, job: JobListing):
        self.add_line_to_status(f"Loading Job Description for {job.title}...")
        self.add_line_to_status("• Scraping job link...")

        # Scrape job link to get full description
        try:
            raw_job_description = await scrape_job_info(job.link)
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
        
        sleep(0.5)  # small pause for effect
        self.status_label.text = ""  # clear status
        self.add_line_to_status(f"Job Title: {job.title}")
        self.add_line_to_status(f"Company: {job.company}")
        self.add_line_to_status(f"Location: {job.location}")
        self.add_line_to_status(f"Description: {job_description}")


    def on_show(self, job: JobListing):
        asyncio.create_task(self.load_job(job)) 