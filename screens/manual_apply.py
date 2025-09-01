import asyncio
import logging
import textwrap
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.layout import Layout, HSplit, Window
from prompt_toolkit.layout.controls import FormattedTextControl
from prompt_toolkit.widgets import TextArea, Label
from screens.screen_base import Screen

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
            height=3,
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

    async def process_job(self):
        """Process the job application"""
        self.status_label.text = "Processing job application..."
        self.redraw()
        
        try:
            # Validate input
            is_valid, error_msg = self.validate_url()
            if not is_valid:
                self.status_label.text = f"Error: {error_msg}"
                self.redraw()
                return
            
            url = self.get_url()
            
            # Here you would call your job processing logic
            # For example:
            # from fill_resume import fill_resume
            # result = await fill_resume(url)
            
            # Placeholder for actual processing
            await asyncio.sleep(2)  # Simulate processing time
            
            self.status_label.text = f"✓ Successfully processed job from URL"
            self.redraw()
            
            # Optionally clear input after successful processing
            # self.clear_input()
            
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
        get_app().layout.focus(self.url_input)