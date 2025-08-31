import asyncio
import logging
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.layout import Layout, HSplit, Window
from prompt_toolkit.layout.controls import FormattedTextControl
from screens.screen_base import Screen
from prompt_toolkit.application import get_app
from scraping.get_jobs import scrape_jobs
from ai.parse_job_listings import parse_job_listings

from models.job_listing import JobListing

ascii_art = r"""
___________.__            .___      ____.     ___.           
╲_   _____╱│__│ ____    __│ _╱     │    │ ____╲_ │__   ______
 │    __)  │  │╱    ╲  ╱ __ │      │    │╱  _ ╲│ __ ╲ ╱  ___╱
 │     ╲   │  │   │  ╲╱ ╱_╱ │  ╱╲__│    (  <_> ) ╲_╲ ╲╲___ ╲ 
 ╲___  ╱   │__│___│  ╱╲____ │  ╲________│╲____╱│___  ╱____  >
     ╲╱            ╲╱      ╲╱                      ╲╱     ╲╱ 
"""

def get_job_text(job: JobListing):
    lines = [f"Title: {job.title}"]
    lines.append(f"Company: {job.company or 'N/A'}")
    lines.append(f"Location: {job.location or 'N/A'} | Salary: {job.salary or 'N/A'}")
    lines.append(f"Time Listed: {job.time_listed or 'N/A'}")
    if job.description:
        lines.append("\nDescription:")
        lines.append(job.description)

    return "\n".join(lines)

class FindJobsScreen(Screen):
    def __init__(self):
        super().__init__("find_jobs")
        self.control = FormattedTextControl(self.render, focusable=True)
        self.container = HSplit([Window(content=self.control, always_hide_cursor=True)])
        self.jobs: list[JobListing] = []
        # self.jobs = jobs  # temp for now
        self.jobs = []
        self.current_job_index = 0 
        self.loading = False  # Initialize loading state 

    def on_show(self):
        if len(self.jobs) == 0:
            self.loading = True
            asyncio.create_task(self.load_jobs())

    async def load_jobs(self):
        try:
            with self.suppress_output():
                scrape_result = await scrape_jobs()

                # Process the scrape_result and update self.jobs
                parsed = parse_job_listings(scrape_result)
                self.jobs = parsed.jobs
        except Exception as e:
            # Handle any errors silently to avoid TUI interference
            logging.error(f"Error loading jobs: {e}")
            self.jobs = []  # Set empty list on error

        self.loading = False
        # Use app.invalidate() instead of control.invalidate()
        get_app().invalidate()

    def render(self):
        frags = []
        
        frags.append(("", ascii_art))
        frags.append(("", "\n" + "="*self.line_len + "\n"))

        if self.loading:
            frags.append(("", "Loading jobs...\n"))
            frags.extend(self.get_default_controls())
            return frags

        if not self.jobs:
            frags.append(("", "No jobs found.\n"))
            frags.extend(self.get_default_controls())
            return frags
        
        if self.current_job_index >= len(self.jobs):
            self.current_job_index = len(self.jobs) - 1
        
        current_job = self.jobs[self.current_job_index]
        job_text = get_job_text(current_job)
        
        # Add navigation info
        nav_info = f"\nJob {self.current_job_index + 1} of {len(self.jobs)}"
        nav_help = "\nPress 'j' for next job, 'k' for previous job, 'q' to go back"
        
        frags.append(("", job_text + "\n"))
        frags.append(("", "\n" + "="*self.line_len))
        frags.append(("", nav_info + nav_help))

        return frags
       
    def layout(self):
        return Layout(self.container)
   
    def keybindings(self, app_state=None):
        kb = KeyBindings()
        
        @kb.add("q")
        def _(event):
            app_state.switch_screen("landing")
        
        @kb.add("j")  # next job
        def _(event):
            self.current_job_index = (self.current_job_index + 1) % len(self.jobs)
            event.app.invalidate()
        
        @kb.add("k")  # previous job
        def _(event):
            self.current_job_index = (self.current_job_index - 1) % len(self.jobs)
            event.app.invalidate()

        return kb