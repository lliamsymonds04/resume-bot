import os

def get_text_folder() -> str:
    # make it if it doesnt exist
    os.makedirs("texts", exist_ok=True)
    return "texts"

def append_filename_to_folder(filename: str) -> str:
    filename = filename if filename.endswith(".txt") else f"{filename}.txt"
    folder = get_text_folder()
    return os.path.join(folder, filename)

def save_text(text: str, filename: str) -> None:
    """Save text to a file."""
    filename = append_filename_to_folder(filename)
    with open(filename, "w", encoding="utf-8") as f:
        f.write(text)


def load_text(filename: str) -> str:
    """Load text from a file."""
    filename = append_filename_to_folder(filename)
    with open(filename, "r", encoding="utf-8") as f:
        return f.read()