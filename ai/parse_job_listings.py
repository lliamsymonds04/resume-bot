from models.job_listing import JobListing
from langchain_core.output_parsers import PydanticOutputParser
from pydantic import BaseModel
from ai.llm_config import get_llm




class JobListingsResponse(BaseModel):
    jobs: list[JobListing]

def parse_job_listings(job_listings: str) -> JobListingsResponse:
    llm = get_llm()

    parser = PydanticOutputParser(pydantic_object=JobListingsResponse)

    prompt = f"""
    Please extract job listings from the following text:

    {job_listings}

    Format instructions:
    {parser.get_format_instructions()}
    """

    response = llm.invoke(prompt)

    try:
        parsed = parser.parse(response.content)
        return parsed
    except Exception as e:
        print(f"Failed to parse LLM output: {e}")
        # Optionally, you can add retry logic here
        return None