import asyncio
import logging
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.layout import Layout, HSplit, Window
from prompt_toolkit.layout.controls import FormattedTextControl
from prompt_toolkit.widgets import TextArea, Label
from ai.parse_job import parse_job_description
from scraping.scrape_job_info import scrape_job_info
from screens.screen_base import Screen
from make_resume import fill_resume, save_resume
from make_cover_letter import make_cover_letter, save_cover_letter
from ai.resume_util import get_input_data

ascii_art = r"""
   _____                             .__       _____             .___      
  /     \ _____    ____  __ _______  |  |     /     \   ____   __| _/____  
 /  \ /  \\__  \  /    \|  |  \__  \ |  |    /  \ /  \ /  _ \ / __ |/ __ \ 
/    Y    \/ __ \|   |  \  |  // __ \|  |__ /    Y    (  <_> ) /_/ \  ___/ 
\____|__  (____  /___|  /____/(____  /____/ \____|__  /\____/\____ |\___  >
        \/     \/     \/           \/               \/            \/    \/ 
"""

class ManualApplyScreen(Screen):
    def __init__(self):
        super().__init__("manual_apply")
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
            Label(text="Job URL (enter the full URL of the job posting):"),
            self.url_input,
            Label(text=""),  # Spacer
            self.status_label,
            Label(text=""),  # Spacer
            Label(text="Press Enter to process job | Press Ctrl+C to clear | Press 'q' to go back"),
        ])
        
        # Main container
        self.container = HSplit([
            header,
            Window(height=1),  # Separator
            form_content,
        ])

    def render_header(self):
        frags = []
        frags.append(("", ascii_art))
        frags.append(("", "\n" + "="*self.line_len + "\n"))
        frags.append(("", "Enter a job URL to generate a tailored resume:\n"))
        return frags

    def layout(self):
        return Layout(self.container)

    def clear_input(self):
        """Clear the URL input field"""
        self.url_input.text = ""
        self.status_label.text = ""

    def get_url(self):
        """Get the current URL input"""
        return self.url_input.text.strip()

    def validate_url(self):
        """Validate the URL input"""
        url = self.get_url()
        if not url:
            return False, "Please enter a job URL"
        
        # Basic URL validation
        if not (url.startswith("http://") or url.startswith("https://")):
            return False, "Please enter a valid URL (must start with http:// or https://)"
        
        return True, ""

    def add_line_to_status(self, line):
        """Add a line to the status label"""
        if self.status_label.text:
            self.status_label.text += "\n"
        self.status_label.text += line
        self.redraw()

    async def process_job(self):
        """Process the job application"""
        
        try:
            # Validate input
            is_valid, error_msg = self.validate_url()
            if not is_valid:
                self.status_label.text = f"Error: {error_msg}"
                self.redraw()
                return
            
            url = self.get_url()
            self.add_line_to_status(f"• Scraping the url...")
            
            with self.suppress_output():
                job_info = await scrape_job_info(url)

            self.add_line_to_status(f"• Processing job information...")
            job_description = parse_job_description(job_info)

            self.add_line_to_status(f"✓ Successfully processed job from URL")
            self.add_line_to_status(f"• Tailoring skills...")

            input_data = await get_input_data(job_description)

            self.add_line_to_status(f"✓ Skills tailored successfully")
            self.add_line_to_status(f"• Generating resume...")
            
            resume = await fill_resume(input_data)
            save_resume(resume, job_description.company, keep_md=True)
            
            self.add_line_to_status(f"✓ Successfully generated resume")
            self.add_line_to_status(f"• Generating cover letter...")

            cover_letter = await make_cover_letter(input_data)
            save_cover_letter(cover_letter, job_description.company, keep_md=True)
            
            self.add_line_to_status(f"✓ Successfully generated cover letter")
            self.add_line_to_status(f"✓ All done! Check the output folder for your files.")

        except Exception as e:
            logging.error(f"Error processing job: {e}")
            self.status_label.text = f"Error: Failed to process job application"
            self.redraw()

    def keybindings(self, app_state=None):
        kb = KeyBindings()

        @kb.add("q")
        def _(event):
            app_state.switch_screen("landing")

        @kb.add("enter")
        def _(event):
            # Process the job when Enter is pressed
            asyncio.create_task(self.process_job())

        @kb.add("c-c")  # Ctrl+C
        def _(event):
            # Clear input
            self.clear_input()
            self.redraw()

        return kb

    def on_show(self):
        """Called when the screen is shown - focus the URL input"""
        from prompt_toolkit.application import get_app
        self.clear_input()
        get_app().layout.focus(self.url_input)