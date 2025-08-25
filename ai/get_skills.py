import json
from pydantic import BaseModel
from typing import List
from langchain_core.output_parsers import PydanticOutputParser
from llm_config import get_llm
import datetime

class CategorizedSkillsResponse(BaseModel):
    programming_languages: List[str]
    frameworks_libraries: List[str] 
    tools: List[str]
    soft_skills: List[str]
    education_certifications: List[str]


def get_skills(use_cache: bool = True) -> CategorizedSkillsResponse:
    now = datetime.datetime.now()

    if use_cache:
        #check if cache exists
        try:
            with open("data/skills_cache.json") as f:
                # get the date of the cache
                data = json.load(f)
                if "date" in data:
                    cache_date = data["date"]
                    # convert to datetime
                    cache_date = datetime.datetime.fromisoformat(cache_date)
                    if now - cache_date < datetime.timedelta(days=1):
                        return CategorizedSkillsResponse(**data["skills"])

        except FileNotFoundError:
            pass

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
    
    parser = PydanticOutputParser(pydantic_object=CategorizedSkillsResponse)
    prompt = f"""
    Please extract and categorize relevant skills from the following information:
    Base Skills: {base_skills}
    Projects: {projects}
    Coursework: {coursework}
    Experience: {experience}
    Me: {me}
    
    Categorize skills into:
    - programming_languages: .
    - frameworks_libraries: .
    - tools: SQL, MongoDB, Docker, AWS, Git, Jira, etc.
    - soft_skills: From every thing stated determine all the soft skills i have. i am excellent.
    - education_certifications: Degrees, certificates, etc.
    
    {parser.get_format_instructions()}
    """
    response = llm.invoke(prompt)
    parsed = parser.parse(response.content)

    # skills = parsed.skills
    skills_dict = parsed.model_dump()
    
    # Cache the result
    with open("data/skills_cache.json", "w") as f:
        json.dump({"date": now.isoformat(), "skills": skills_dict}, f)

    # return skills_dict
    return parsed

if __name__ == "__main__":
    skills = get_skills()
    print("Extracted Skills:")
    for category, skills in skills.model_dump().items():
        print(f"{category}:")
        for skill in skills:
            print(f" - {skill}")