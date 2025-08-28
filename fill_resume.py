import json
from ai.parse_job_description import parse_job_description
from ai.get_skills import get_relevant_skills
from ai.llm_config import get_llm
from ai.tailor_projects import tailor_projects
from models.job_description import JobDescription
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

from scraping.scrape_job_info import scrape_job_info
from util.text_util import load_text, save_text


def load_resume_template(filename: str = "resume/resume_template.typ"):
    with open(filename, 'r', encoding='utf-8') as f:
        return f.read()

def create_resume_filling_prompt():
    """
    Creates the ChatPromptTemplate for filling the Typst resume.
    """
    prompt = ChatPromptTemplate.from_template("""
        You are a resume-tailoring expert. Your task is to fill a Typst resume template with professional information tailored specifically for a given job description.

        ---

        **Provided Information:**

        **Job Description:**
        {job_description}

        **My Data (JSON format):**
        {my_data}

        **Relevant Skills:**
        {relevant_skills}

        **Tailored Projects:**
        {tailored_projects}

        **Instructions:**

        1.  **Goal:** Generate a single, complete Typst function call to `resume-template()` with all arguments populated.
        2.  **Summary:** Re-write the `summary` section from "My Data" to be concise and directly relevant to the job description. Highlight key skills and experiences mentioned in the job post.
        3.  **Experience:** For each experience entry in "My Data," rewrite the bullet points to align with the job's requirements and keywords. Focus on quantifiable achievements.
            if you cannot find any experience do not list it
        4.  **Skills:** Populate the `skills` array with the provided "Relevant Skills."
        5.  **Projects:** Populate the `projects` array with the provided "Tailored Projects."
        6.  **Do NOT:**
            -   Add any extra text, explanations, or markdown outside of the `resume-template()` function call.
            -   Invent or hallucinate any information not present in the provided data.
            -   Change the structure of the `resume-template()` function call.
            -   Encapsulate the output in a markdown code block.

        escape special characters for formatting like # and @

        ---

        **Expected Output:**

        Provide only the `resume-template(...)` function call with the correct Typst syntax and arguments filled with the tailored information.
        """)

    return prompt

def fill_resume(job_description: JobDescription):
    template = load_resume_template()
    # Here you would add logic to fill in the template with user data

    # get the relevant skills
    relevant_skills = get_relevant_skills(job_description)

    # tailor the projects
    tailored_projects = tailor_projects(job_description, 3)

    # load the me json
    with open("data/me.json", 'r', encoding='utf-8') as f:
        me_data = json.load(f)

    prompt = create_resume_filling_prompt()
    
    input_data = {
        "job_description": job_description,
        "my_data": me_data,
        "relevant_skills": relevant_skills,
        "tailored_projects": tailored_projects
    }

    llm = get_llm(0.3, "good")
    resume_chain = prompt | llm | StrOutputParser()

    result = resume_chain.invoke(input_data)
    return result

if __name__ == "__main__":
    import os
    if os.path.exists("texts/job_info.txt"):
        with open("texts/job_info.txt", "r") as f:
            # job_info = f.read()
            job_info = load_text("job_info")
    else:
        raise ValueError("No job info found, please run tailor.py first")

    llm = get_llm()
    job_d = parse_job_description(job_info, llm)

    result = fill_resume(job_d)
    print(result)

    with open("resume/generated_resume.typ", "w", encoding="utf-8") as f:
        f.write(result)

    import subprocess

    subprocess.run(["typst", "compile", "resume/generated_resume.typ", "resume/generated_resume.pdf"], check=True)
