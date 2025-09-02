from models.job_description import JobDescription
from ai.get_skills import get_relevant_skills
from ai.tailor_projects import tailor_projects
import json

def remove_code_block(text: str) -> str:
    lines = text.strip().split('\n')

    # Check if the first and last lines are code block delimiters
    if lines[0].startswith("```") and lines[-1] == "```":
        # Remove the first and last lines to get the pure code
        clean_content = "\n".join(lines[1:-1])
    else:
        clean_content = text

    return clean_content

def get_input_data(job_description: JobDescription):
    # get the relevant skills
    relevant_skills = get_relevant_skills(job_description)

    # tailor the projects
    tailored_projects = tailor_projects(job_description, 3)

    # load the me json
    with open("data/me.json", 'r', encoding='utf-8') as f:
        me_data = json.load(f)

    # load coursework
    with open("data/coursework.json", 'r', encoding='utf-8') as f:
        coursework = json.load(f)

    input_data = {
        "job_description": job_description,
        "my_data": me_data,
        "relevant_skills": relevant_skills,
        "tailored_projects": tailored_projects,
        "coursework": coursework
    }

    return input_data