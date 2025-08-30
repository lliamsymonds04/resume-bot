from prompt_toolkit import Application
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.layout import Layout, HSplit, Window
from prompt_toolkit.layout.controls import FormattedTextControl

def render():
    frags = []
    frags.append(("", "Hello, World!\n"))
    
    return frags
    
control = FormattedTextControl(render, focusable=True)
container = HSplit([Window(content=control, always_hide_cursor=True)])


kb = KeyBindings()

@kb.add("q")
def _(event):
    event.app.exit()


app = Application(layout=Layout(container), key_bindings=kb, full_screen=True)


if __name__ == "__main__":
    app.run()