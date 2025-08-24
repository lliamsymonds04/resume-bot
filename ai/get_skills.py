import json
from pydantic import BaseModel
from typing import List
from langchain_core.output_parsers import PydanticOutputParser
from llm_config import get_llm

class SkillsResponse(BaseModel):
    skills: List[str]


def get_skills() -> list[str]:
    with open("data/skills.json") as f:
        base_skills = json.load(f)

    with open("data/projects.json") as f:
        projects = json.load(f)
        
    with open("data/coursework.json") as f:
        coursework = json.load(f)
        
    with open("data/experience.json") as f:
        experience = json.load(f)

    with open("data/me.json") as f:
        me = json.load(f)

    #use ai to add to skills list
    llm = get_llm()
    
    parser = PydanticOutputParser(pydantic_object=SkillsResponse)
    prompt = f"""
    Please extract relevant skills from the following information:

    Base Skills: {base_skills}
    Projects: {projects}
    Coursework: {coursework}
    Experience: {experience}
    Me: {me}

    Also include relevant soft skills. 
    Include education and any certifications.

    Format instructions:
    one skill per entry
    {parser.get_format_instructions()}
    """

    response = llm.invoke(prompt)

    parsed = parser.parse(response.content)
    return parsed.skills

if __name__ == "__main__":
    skills = get_skills()
    print("Extracted Skills:")
    for skill in skills:
        print(f"- {skill}")