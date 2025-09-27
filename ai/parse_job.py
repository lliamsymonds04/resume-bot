from models.job_listing import JobListing
from models.job_description import JobDescription
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
        # Log error instead of printing to avoid TUI interference
        import logging
        logging.error(f"Failed to parse LLM output: {e}")
        return None

def parse_job_description(description: str) -> JobDescription:
    # Use the LLM to parse the job description
    parser = PydanticOutputParser(pydantic_object=JobDescription)
    llm = get_llm()

    prompt = f"""
    Extract the following job description into a structured JSON.
    Do not include anything like pty or ltd in the job title or company name.
    
    Format Instruction: {parser.get_format_instructions()}

    Job Description:
    {description}
    """

    response = llm.invoke(prompt)
    job = parser.parse(response.content)

    return job
