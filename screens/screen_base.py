from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.layout import Layout
from prompt_toolkit.widgets import TextArea, Box

LINE_LEN = 70
class Screen:
    def __init__(self, name):
        self.name = name
        self.line_len = LINE_LEN

    def layout(self):
        """Return the screen's layout"""
        return Layout(Box(TextArea(text=f"This is {self.name}")))

    def keybindings(self, app_state):
        """Return screen-specific keybindings"""
        kb = KeyBindings()
        return kb

    def get_default_controls(self):
        if self.name == "landing":
            q_action = "quit"
        else:
            q_action = "back"

        controls = [
            ("", "\n" + "="*self.line_len),
            ("", f"\n[j] down, [k] up, [enter] select, [q] {q_action}.\n")
        ]
        return controls
    
    def render_options(self):
        result = []
        # render options
        for i, option in enumerate(self.options):
            prefix = "👉 " if i == self.state["selection"] else "   "
            style = "reverse" if i == self.state["selection"] else ""
            result.append((style, f"{prefix}{option}\n"))

        return result

    def bind_move_options(self, kb: KeyBindings):
        @kb.add("j")
        def _(event):
            self.state["selection"] = (self.state["selection"] + 1) % len(self.options)
            self.control.text = self.render()
            event.app.invalidate()

        @kb.add("k")
        def _(event):
            self.state["selection"] = (self.state["selection"] - 1) % len(self.options)
            self.control.text = self.render()
            event.app.invalidate()