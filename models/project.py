from typing import Optional
from pydantic import BaseModel

class Project(BaseModel):
    title: str
    description: str
    github: Optional[str] = None
    website: Optional[str] = None
    youtube: Optional[str] = None