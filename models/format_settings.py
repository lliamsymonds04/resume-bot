import json
import os

settings_path = os.path.join(os.path.dirname(__file__), "..", "data", "format_settings.json")

class FormatSettings:
    def __init__(self, font_size=10, font="Arial", font_stretch=0.8):
        self.font_size = font_size
        self.font = font
        self.font_stretch = font_stretch

    @classmethod
    def from_dict(cls, data):
        return cls(
            font_size=data.get("font_size", 10),
            font=data.get("font", "Arial"),
            font_stretch=data.get("font_stretch", 0.8)
        )

def get_format_settings(type: str) -> FormatSettings:
    with open(settings_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    if type in data:
        return FormatSettings.from_dict(data[type])
    else:
        raise ValueError(f"Format settings for type '{type}' not found.")