from prompt_toolkit import Application
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.layout import Layout, HSplit, Window
from prompt_toolkit.layout.controls import FormattedTextControl

ascii_art = r"""__________                                     __________        __   
\______   \ ____   ________ __  _____   ____   \______   \ _____/  |_ 
 |       _// __ \ /  ___/  |  \/     \_/ __ \   |    |  _//  _ \   __\
 |    |   \  ___/ \___ \|  |  /  Y Y  \  ___/   |    |   (  <_> )  |  
 |____|_  /\___  >____  >____/|__|_|  /\___  >  |______  /\____/|__|  
        \/     \/     \/            \/     \/          \/             """
ascii_art += "\n" + "="*70 + "\n"

def render():
    frags = []
    frags.append(("", ascii_art))
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