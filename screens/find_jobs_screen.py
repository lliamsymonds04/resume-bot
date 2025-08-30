from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.layout import Layout, HSplit, Window, ScrollablePane
from prompt_toolkit.layout.controls import FormattedTextControl
from screens.screen_base import Screen

from models.job_description import JobDescription

ascii_art = r"""
___________.__            .___      ____.     ___.           
╲_   _____╱│__│ ____    __│ _╱     │    │ ____╲_ │__   ______
 │    __)  │  │╱    ╲  ╱ __ │      │    │╱  _ ╲│ __ ╲ ╱  ___╱
 │     ╲   │  │   │  ╲╱ ╱_╱ │  ╱╲__│    (  <_> ) ╲_╲ ╲╲___ ╲ 
 ╲___  ╱   │__│___│  ╱╲____ │  ╲________│╲____╱│___  ╱____  >
     ╲╱            ╲╱      ╲╱                      ╲╱     ╲╱ 
"""

jobs = [
    JobDescription(
        title="Software Engineer",
        company="TechCorp",
        location="Sydney",
        responsibilities=["Develop software", "Review code"],
        requirements=["3+ years experience", "Python proficiency"],
        skills=["Python", "Git", "Docker"],
        salary="$100k-$120k"
    ),
    JobDescription(
        title="Data Scientist",
        company="DataCo",
        location="Melbourne",
        responsibilities=["Analyze data", "Build ML models"],
        requirements=["2+ years experience", "ML knowledge"],
        skills=["Python", "Pandas", "Scikit-learn"],
        salary="$90k-$110k"
    )
]

def get_job_text(job: JobDescription):
    lines = [
        f"Title: {job.title} | Company: {job.company or 'N/A'} | Location: {job.location or 'N/A'} | Salary: {job.salary or 'N/A'}",
        "",
        "Responsibilities:",
    ] + [f"  - {r}" for r in job.responsibilities] + [
        "",
        "Requirements:",
    ] + [f"  - {r}" for r in job.requirements] + [
        "",
        "Skills:",
    ] + [f"  - {s}" for s in job.skills]

    return "\n".join(lines)

class FindJobsScreen(Screen):
    def __init__(self):
        super().__init__("find_jobs")
        self.control = FormattedTextControl(self.render, focusable=True)
        self.container = HSplit([Window(content=self.control, always_hide_cursor=True)])
        self.jobs: list[JobDescription] = []
        self.jobs = jobs  # temp for now
        self.current_job_index = 0 
    
    def render(self):
        frags = []
        
        frags.append(("", ascii_art))
        frags.append(("", "\n" + "="*self.line_len + "\n"))

        if not self.jobs:
            return [("", "No jobs found.")]
        
        if self.current_job_index >= len(self.jobs):
            self.current_job_index = len(self.jobs) - 1
        
        current_job = self.jobs[self.current_job_index]
        job_text = get_job_text(current_job)
        
        # Add navigation info
        nav_info = f"\nJob {self.current_job_index + 1} of {len(self.jobs)}"
        nav_help = "\nPress 'j' for next job, 'k' for previous job, 'q' to go back"
        
        frags.append(("", job_text + "\n"))
        frags.append(("", "\n" + "="*self.line_len))
        frags.append(("", (nav_info + nav_help)))

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