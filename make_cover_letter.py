import os
import subprocess
import json
import asyncio
from datetime import datetime
from dotenv import load_dotenv
from models.job_description import JobDescription
from ai.resume_util import get_input_data, remove_code_block
from ai.llm_config import get_llm
from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

def make_prompt():
    prompt = ChatPromptTemplate.from_template("""
    You are an expert cover letter writer who crafts professional, polished, and ATS-friendly markdown cover letters.

    Provided data:

    Job Description:
    {job_description}

    My Data (JSON):
    {my_data}

    Relevant Skills:
    {relevant_skills}

    Tailored Projects:
    {tailored_projects}

    Coursework:
    {coursework}

    Instructions:
    - Make the title the candidate's name from `my_data`
    - Include the contact information from `my_data`. Format websites in Markdown so that they are clickable links: [url](URL). 
        Example: LinkedIn: [linkedin.com/in/username](https://linkedin.com/in/username)
    - Include phone number with ph: in front
    - Make sure each bit of contact information is on a new line using two spaces 
    - Use \hrulefill to separate the links from the main content
    - Include today's date, {todays_date}
    - Produce a single, complete markdown cover letter addressed to the hiring team. Do NOT include any explanations, comments, or extra text.
    - Keep formatting clean and consistent with Markdown. Avoid code blocks.
    - The cover letter must be well-structured: opening greeting, strong introduction tailored to the job, body paragraphs highlighting skills, projects, and coursework aligned with the role, and a confident closing statement.
    - Ensure the tone is professional, concise, and engaging.
    - Emphasize quantifiable achievements, relevant experiences, and how they align with the company’s needs.
    - Use two lines to separate paragraphs.
    - Use the two spaces at the end of a line to separate lines
    - End with a courteous sign-off (e.g., “Sincerely,”) and the candidate’s full name. Make sure the sign-off and the name are on different lines using two spaces
    """)

    return prompt

async def make_cover_letter(input_data):
    prompt = make_prompt()
    # Call the LLM with the prompt and return the response
    llm = get_llm(0.3, "good")
    chain = prompt | llm | StrOutputParser()
    
    result = await chain.ainvoke(input_data)
    result = remove_code_block(result)
    return result

def save_resume(resume: str, job_description: JobDescription, keep_md = False):
    user_name = "temp"
    with open("data/me.json", 'r', encoding='utf-8') as f:
        me_data = json.load(f)
        user_name = me_data.get("name", "temp").lower()

    base_path = f"output/{job_description.company}"

    # Replace spaces with hyphens
    user_name = user_name.replace(" ", "-")
    base_path = base_path.replace(" ", "-")
    os.makedirs(base_path, exist_ok=True)

    md_file_path = f"{base_path}/generated-cover-letter.md"
    with open(md_file_path, "w", encoding="utf-8") as f:
        f.write(resume)

    subprocess.run([
        "pandoc",
        md_file_path,
        "-o", f"{base_path}/{user_name}-cover-letter.pdf",
        "--pdf-engine=xelatex",
        "-V", "geometry:margin=1in",
        "-V", "fontsize=11pt",
        "-V", "geometry:top=0.5in",
        # "-V", "mainfont=Garamond",
        "-V", "pagestyle=empty"
    ], check=True)

    # delete the markdown file
    if not keep_md:
        os.remove(md_file_path)


if __name__ == "__main__":
    load_dotenv()
    job = JobDescription(
        title="Senior Data Engineer",
        company="NovaFin Analytics",
        location="Brisbane, QLD (Hybrid)",
        responsibilities=[
            "Architect, build and maintain ETL/ELT pipelines",
            "Design data models and maintain the data warehouse",
            "Collaborate with ML engineers to productionize models",
            "Implement data quality checks and monitoring"
        ],
        requirements=[
            "3+ years in data or backend engineering",
            "Strong Python and SQL skills (pandas, SQLAlchemy)",
            "Experience with Spark or other distributed frameworks",
            "Familiarity with cloud platforms (AWS/GCP/Azure) and Airflow/dbt"
        ],
        skills=["Python", "SQL", "Spark", "Airflow", "dbt", "Docker", "CI/CD"],
        salary="AUD 110,000 - 130,000"
    )

    input_data = get_input_data(job)

    cover_letter = asyncio.run(make_cover_letter(input_data))

    save_resume(cover_letter, job, keep_md=True)

    


