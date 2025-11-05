import json
from ai.llm_config import get_llm
from models.job_description import JobDescription
from models.project import Project
from langchain_core.documents import Document
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.output_parsers import PydanticOutputParser
from pydantic import BaseModel


class Projects(BaseModel):
    projects: list[Project]


projects_parser = PydanticOutputParser(pydantic_object=Projects)


def generate_project_prompt():
    prompt = """
    You are a resume tailoring expert. Your task is to pick the {num_projects} most relevant projects from the provided list based on the given job description.
    Always choose harder projects over easier ones.
    Focus on projects that best align with the skills, experiences, and requirements outlined in the job description.
    Also, expand on the project to make it more relevant to the job description.
    Do not change the title. Do not lie about my skills or process
    Always mention the programming languages and the tools used
    Do not talk about external teams or stakeholders if none are mentioned
    
    Job Description:
    {job_description}
    
    Projects:
    {projects}
    
    Format instructions:
    {format_instructions}
    """
    return prompt


async def tailor_projects(job_description: JobDescription, num_projects: int = 3):
    with open("data/projects.json", "r") as f:
        projects_raw = json.load(f)

    prompt = generate_project_prompt()
    llm = get_llm(0.3)
    response = await llm.ainvoke(
        prompt.format(
            num_projects=num_projects,
            job_description=job_description.model_dump(),
            projects=json.dumps(projects_raw, indent=2),
            format_instructions=projects_parser.get_format_instructions(),
        )
    )

    return projects_parser.parse(response.content)


async def expand_project_for_job(job_description: JobDescription, project: Project):
    llm = get_llm(0.3)

    parser = PydanticOutputParser(pydantic_object=Project)
    prompt = f"""
    Given the following job description:
    {job_description.model_dump()}

    And the project details:
    {project.model_dump()}

    Expand on the project to make it more relevant to the job description.
    Do not change the title
    Do not lie about my skills or process
    Do not talk about programming languages or tools that i did not use.
    Always mention the programming languages and the tools
    Keep the description concise and focused on the key aspects. It is for a resume
    Do not talk about external teams or stakeholders if none are mentioned
    Talk about the cloud technologies used if present in the project

    Format instructions:
    {parser.get_format_instructions()}
    """

    response = await llm.ainvoke(prompt)

    return parser.parse(response.content)


async def expand_projects_for_job(job_description: JobDescription, projects: Projects):
    llm = get_llm(0.3)

    parser = PydanticOutputParser(pydantic_object=Projects)

    prompt = f"""
        Given the following job description:
        {job_description.model_dump()}

        And the projects are:
        {projects.model_dump()}
        you should return a list of expanded projects. There should be {len(projects.projects)}.

        Expand on the projects to make them more relevant to the job description.
        Do not change the title
        Do not lie about my skills or process
        Do not talk about programming languages or tools that i did not use.
        Always mention the programming languages and the tools
        Keep the description concise and focused on the key aspects. It is for a resume
        Do not talk about external teams or stakeholders if none are mentioned

        Format instructions:
        {parser.get_format_instructions()}
        """

    response = await llm.ainvoke(prompt)
    return parser.parse(response.content)

