import asyncio
import logging
import textwrap
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.layout import Layout, HSplit, Window
from prompt_toolkit.layout.controls import FormattedTextControl
from screens.screen_base import Screen
from job_scraping import scrape_jobs
from ai.parse_job import parse_job_listings

from models.job_listing import JobListing

ascii_art = r"""
___________.__            .___      ____.     ___.           
╲_   _____╱│__│ ____    __│ _╱     │    │ ____╲_ │__   ______
 │    __)  │  │╱    ╲  ╱ __ │      │    │╱  _ ╲│ __ ╲ ╱  ___╱
 │     ╲   │  │   │  ╲╱ ╱_╱ │  ╱╲__│    (  <_> ) ╲_╲ ╲╲___ ╲ 
 ╲___  ╱   │__│___│  ╱╲____ │  ╲________│╲____╱│___  ╱____  >
     ╲╱            ╲╱      ╲╱                      ╲╱     ╲╱ 
"""



class FindJobsScreen(Screen):
    def __init__(self):
        super().__init__("find_jobs")
        self.control = FormattedTextControl(self.render, focusable=True)
        self.container = HSplit([Window(content=self.control, always_hide_cursor=True)])
        self.jobs: list[JobListing] = []
        self.current_job_index = 0 
        self.loading = False  # Initialize loading state 
        # self.db = JobDatabase()  # Initialize database service
        self.page = 1

    def on_show(self):
        # First, load existing jobs from database
        self.jobs = self.db.load_jobs(limit=50)  # Load last 50 jobs
        
        # If no jobs in database or user wants fresh data, scrape new ones
        if len(self.jobs) == 0:
            self.loading = True
            asyncio.create_task(self.load_jobs())

    def get_job_text(self, job: JobListing):
        lines = [f"Title: {job.title}"]
        lines.append(f"Company: {job.company or 'N/A'}")
        lines.append(f"Location: {job.location or 'N/A'} | Salary: {job.salary or 'N/A'}")
        lines.append(f"Time Listed: {job.time_listed or 'N/A'}")
        if job.description:
            lines.append("\nDescription:")
            # Wrap the description text to fit within terminal width
            wrapped_description = textwrap.fill(job.description, width=self.line_len, break_long_words=False)
            lines.append(wrapped_description)

        return "\n".join(lines)

    async def load_jobs(self):
        try:
            with self.suppress_output():
                scrape_result = await scrape_jobs(self.page)
                parsed = parse_job_listings(scrape_result)
                
                # Save new jobs to database
                new_jobs_count = self.db.save_jobs(parsed.jobs)
                
                # Load all jobs from database (including newly saved ones)
                self.jobs = self.db.load_jobs(limit=50)
                self.current_job_index = 0  # Reset to first job
                self.page += 1
                
                logging.info(f"Scraped and saved {new_jobs_count} new jobs")
                
        except Exception as e:
            logging.error(f"Error loading jobs: {e}")
            # Fallback to database jobs if scraping fails
            self.jobs = self.db.load_jobs(limit=50)

        self.loading = False
        from prompt_toolkit.application import get_app
        get_app().invalidate()

    def render(self):
        frags = []
        
        frags.append(("", ascii_art))
        frags.append(("", "\n" + "="*self.line_len + "\n"))

        # Show database info
        total_jobs_in_db = self.db.get_job_count()
        frags.append(("", f"Database: {total_jobs_in_db} total jobs stored\n"))

        if self.loading:
            frags.append(("", "Loading new jobs...\n"))
            frags.extend(self.get_default_controls())
            return frags

        if not self.jobs:
            frags.append(("", "No jobs found. Press 'r' to refresh.\n"))
            frags.extend(self.get_default_controls())
            return frags
        
        if self.current_job_index >= len(self.jobs):
            self.current_job_index = len(self.jobs) - 1
        
        current_job = self.jobs[self.current_job_index]
        job_text = self.get_job_text(current_job)
        
        # Add navigation info
        nav_info = f"\nJob {self.current_job_index + 1} of {len(self.jobs)} (showing last 50)"
        nav_help = "\nPress 'j' for next, 'k' for previous, 'r' to refresh, 'q' to go back"
        
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
            if self.jobs:
                self.current_job_index = (self.current_job_index + 1) % len(self.jobs)
                event.app.invalidate()
        
        @kb.add("k")  # previous job
        def _(event):
            if self.jobs:
                self.current_job_index = (self.current_job_index - 1) % len(self.jobs)
                event.app.invalidate()
        
        @kb.add("r")  # refresh - scrape new jobs
        def _(event):
            self.loading = True
            asyncio.create_task(self.load_jobs())
            event.app.invalidate()

        @kb.add("enter")
        def _(event):
            if len(self.jobs) > 0:
                job = self.jobs[self.current_job_index]

                # change to different screen to process job
                app_state.switch_screen("job_description", job=job) 

        return kb