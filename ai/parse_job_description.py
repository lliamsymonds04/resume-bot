from models.job_description import JobDescription
from langchain_core.output_parsers import PydanticOutputParser
from ai.llm_config import get_llm

def parse_job_description(job_description: str) -> JobDescription:
    # Use the LLM to parse the job description
    parser = PydanticOutputParser(pydantic_object=JobDescription)
    llm = get_llm()

    prompt = f"""
    Extract the following job description into a structured JSON.
    
    Format Instruction: {parser.get_format_instructions()}

    Job Description:
    {job_description}
    """

    response = llm.invoke(prompt)
    job = parser.parse(response.content)

    return job
