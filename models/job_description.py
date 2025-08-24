from pydantic import BaseModel
from typing import List, Optional

class JobDescription(BaseModel):
    title: str
    company: Optional[str] = None
    location: Optional[str] = None
    responsibilities: List[str]
    requirements: List[str]
    skills: List[str]
    salary: Optional[str] = None