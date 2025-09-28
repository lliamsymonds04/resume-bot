from typing import Optional
from pydantic import BaseModel

class Experience(BaseModel):
    name: str
    description: str
    role: Optional[str] = None
    time_period: Optional[str] = None
    link: Optional[str] = None