from models.job_description import JobDescription
from langchain_groq import ChatGroq
from langchain_core.output_parsers import PydanticOutputParser

def parse_job_description(job_description: str, llm: ChatGroq) -> JobDescription:
    # Use the LLM to parse the job description
    parser = PydanticOutputParser(pydantic_object=JobDescription)

    prompt = f"""
    Extract the following job description into a structured JSON.
    
    Format Instruction: {parser.get_format_instructions()}

    Job Description:
    {job_description}
    """

    response = llm.invoke(prompt)
    job = parser.parse(response.content)

    return job
