import subprocess
from models.job_description import JobDescription
from ai.get_skills import get_relevant_skills
from ai.tailor_projects import tailor_projects
from datetime import datetime
import json
import os

def remove_code_block(text: str) -> str:
    lines = text.strip().split('\n')

    # Check if the first and last lines are code block delimiters
    if lines[0].startswith("```") and lines[-1] == "```":
        # Remove the first and last lines to get the pure code
        clean_content = "\n".join(lines[1:-1])
    else:
        clean_content = text

    return clean_content

def ordinal(n: int) -> str:
    if 11 <= n % 100 <= 13:  # special case for 11th, 12th, 13th
        suffix = "th"
    else:
        suffix = {1: "st", 2: "nd", 3: "rd"}.get(n % 10, "th")
    return f"{n}{suffix}"

def get_date():
    now = datetime.now()
    return f"{now.strftime('%B')} {ordinal(now.day)}, {now.year}"

async def get_input_data(job_description: JobDescription):
    # get the relevant skills
    relevant_skills = await get_relevant_skills(job_description)

    # tailor the projects
    tailored_projects = await tailor_projects(job_description, 3)

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
        "coursework": coursework,
        "todays_date": get_date()
    }

    return input_data

def save_md_to_pdf(md: str, job_description: JobDescription, tail_name: str, keep_md: bool, additional_args: list):
    user_name = "temp"
    with open("data/me.json", 'r', encoding='utf-8') as f:
        me_data = json.load(f)
        user_name = me_data.get("name", "temp").lower()

    base_path = f"output/{job_description.company}"

    # Replace spaces with hyphens
    user_name = user_name.replace(" ", "-")
    base_path = base_path.replace(" ", "-")
    os.makedirs(base_path, exist_ok=True)

    md_file_path = f"{base_path}/generated-{tail_name}.md"
    with open(md_file_path, "w", encoding="utf-8") as f:
        f.write(md)

    args = [
        "pandoc",
        md_file_path,
        "-o", f"{base_path}/{user_name}-cover-letter.pdf",
        "--pdf-engine=xelatex",
        "-V", "geometry:margin=1in",
        "-V", "geometry:top=0.5in",
        "-V", "pagestyle=empty"
    ]

    args.extend(additional_args)

    subprocess.run(args, check=True)

    # delete the markdown file
    if not keep_md:
        os.remove(md_file_path)

