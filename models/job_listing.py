from typing import Optional
from pydantic import BaseModel


class JobListing(BaseModel):
    title: str
    link: str
    company: Optional[str]
    location: Optional[str]
    description: Optional[str]
    salary: Optional[str]
    time_listed: Optional[str]