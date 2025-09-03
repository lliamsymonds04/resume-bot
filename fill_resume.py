import json
import os
import subprocess
from ai.parse_job import parse_job_description
from ai.llm_config import get_llm
from ai.resume_util import get_input_data, remove_code_block
from models.job_description import JobDescription
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

from util.text_util import load_text

def create_resume_filling_prompt():
    """
    Creates the ChatPromptTemplate for filling the Typst resume.
    """
    prompt = ChatPromptTemplate.from_template("""
        You are a resume-tailoring expert for ATS. Your task is to fill a markdown resume template with professional information tailored specifically for a given job description.

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

        **Coursework:**
        {coursework}

        **Instructions:**

        **Goal:** Generate a markdown resume.
        1.  Make the title my name. Make sure to add a space between the markdown then add a new line.
        2.  Format my contact details in one line and embedded the websites. Make the text for my website not have https or www.
            (email, phone number, website, linkedin)
        3.  Add \hrulefill to separate contact and the below sections
        4.  **Summary:** Re-write the `summary` section from "My Data" to be concise and directly relevant to the job description. Highlight key skills and experiences mentioned in the job post.
            Do not directly mention the company or the position title.
        5.  **Education:** Populate the `education` array with the relevant information from "My Data.". Include a summary of relevant coursework i have completed. Change it to fit the job description.
        6.  **Skills:** make dotpoints containing the relevant skills categorised. Use the categories given. Fill them horizontally to save space
        7.  **Projects:** Populate the `projects` array with the provided "Tailored Projects." Use dotpoints to give points on each project and put the links on a new line, horizontally
        8.  Always use \hrulefill to separate each sections.
        9.  **Do NOT:**
            -   Add any extra text, explanations, or images or embedded images.
            -   Invent or hallucinate any information not present in the provided data.

        ---

        **Expected Output:**

        Provide only the markdown with the arguments filled with the tailored information.
        """)

    return prompt

async def fill_resume(input_data: dict):
    prompt = create_resume_filling_prompt()

    llm = get_llm(0.3, "light")
    resume_chain = prompt | llm | StrOutputParser()

    result = await resume_chain.ainvoke(input_data)
    result = remove_code_block(result)
    return result

def fix_resume_formatting(resume: str) -> str:
    prompt = ChatPromptTemplate.from_template("""
    Here is my resume in markdown. Fix any spacing or syntax errors. Do not remove horizontal lines
    
    {resume}
    return the markdown resume fixed. Do not comment on what you changed, only return the resume.
    """)

    llm = get_llm(0, "light")
    fix_chain = prompt | llm | StrOutputParser()
    result = fix_chain.invoke({"resume": resume})

    return remove_code_block(result)

def save_resume(resume: str, job_description: JobDescription, keep_md = False):
    base_path = f"output/{job_description.company}"
    os.makedirs(base_path, exist_ok=True)
    with open(f"{base_path}/generated_resume.md", "w", encoding="utf-8") as f:
        f.write(resume)

    #TODO: make the resume save as users name
    user_name = "temp"
    with open("data/me.json", 'r', encoding='utf-8') as f:
        me_data = json.load(f)
        user_name = me_data.get("name", "temp").lower()

    subprocess.run([
        "pandoc",
        f"{base_path}/generated_resume.md",
        "-o", f"{base_path}/{user_name}-resume.pdf",
        "-V", "geometry:margin=1in",
        "-V", "fontsize=10pt",
        "-V", "geometry:top=0.5in",
        "-V", "mainfont=Garamond",
        "-V", "pagestyle=empty"
    ], check=True)

    # delete the markdown file
    if not keep_md:
        os.remove(f"{base_path}/generated_resume.md")

if __name__ == "__main__":
    import os
    if os.path.exists("texts/job_info.txt"):
        with open("texts/job_info.txt", "r") as f:
            job_info = load_text("job_info")
    else:
        raise ValueError("No job info found, please run tailor.py first")

    llm = get_llm()
    job_d = parse_job_description(job_info, llm)

    result = fill_resume(job_d)
    result = fix_resume_formatting(result)

    #save the file
    save_resume(result, job_d)