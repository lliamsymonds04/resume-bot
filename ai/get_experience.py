from ai.llm_config import get_llm
from models.job_description import JobDescription
from models.experience import Experience
from pydantic import BaseModel
from langchain_core.output_parsers import PydanticOutputParser
import json

class Experiences(BaseModel):
    experiences: list[Experience]

experience_parser = PydanticOutputParser(pydantic_object=Experiences)  

def get_experience():
    with open("data/experience.json", 'r', encoding='utf-8') as f:
        experience = json.load(f)

    return experience

def generate_tailor_experience_prompt():
    return """
    You are an expert resume writer.
    Given the following job description, tailor the following experience to better match the job description.
    Return all the experiences. Order them by Descending order of time period.

    # Job Description:
    {job_description}

    # Experience:
    {experience}

    # Format instructions:
    {format_instructions}
    """

async def tailor_experience(job_description: JobDescription):
    experience = get_experience()
    
    prompt = generate_tailor_experience_prompt()
    llm = get_llm(0.3)

    response = await llm.ainvoke(prompt.format(
        job_description=job_description.model_dump(),
        experience=json.dumps(experience, indent=2),
        format_instructions=experience_parser.get_format_instructions()
    ))

    return experience_parser.parse(response.content).experiences