import os
from ai.parse_job import parse_job_description
from ai.llm_config import get_llm
from ai.resume_util import remove_code_block, save_md_to_pdf
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

        **Experience:**
        {experience}

        **Instructions:**

        **Goal:** Generate a markdown resume.
        1.  Make the title my name. Make sure to add a space between the markdown then add a new line.
        2.  Format my contact details in one line and embedded the websites. Make the text for my website not have https or www.
            (email, phone number, website, linkedin)
        3.  Add \hrulefill to separate contact and the below sections.
        4.  **Summary:** Re-write the `summary` section from "My Data" to be concise and directly relevant to the job description. Highlight key skills and experiences mentioned in the job post.
            Do not directly mention the company or the position title.
        5.  **Education:** Populate the `education` array with the relevant information from "My Data." Include the major. Include a summary of relevant coursework i have completed and the course code. Change it to fit the job description. Include no more than 4 courses.
        6.  **Experience:** Populate the `experience` array with the tailored experiences. Use dotpoints to give points on each experience and put the links on a new line, horizontally. If there is no experience do not include this section. Include a website link if it is given and relevant.
        7.  **Skills:** using the 'relevant_skills' provided and the categories, populate each skill category horizontally. Make the skill category name bold. Separate each skill with a comma. Do not use bullet points. End each line with a space and a backslash to make a new line.
        8.  **Projects:** Populate the `projects` array with the provided "Tailored Projects." Use dotpoints to give points on each project and put the links on a new line, horizontally
        9.  Always use \hrulefill to separate each sections. Make each section a h2 header (##).
        10.  **Do NOT:**
            -   Add any extra text, explanations, or images or embedded images.
            -   Invent or hallucinate any information not present in the provided data.

        ---

        **Expected Output:**

        Provide only the markdown with the arguments filled with the tailored information.

        **Additional Notes:**
        {additional_notes}
        """)

    return prompt

async def make_resume(input_data: dict):
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

def get_resume_format_args():
    header_includes = r"""
    \renewcommand{\baselinestretch}{0.8}
    \setlength{\parskip}{0pt}
    \setlength{\itemsep}{0pt}
    \setlength{\topsep}{0pt}
    \setlength{\partopsep}{0pt}
    \setlength{\parsep}{0pt}
    \setlength{\leftmargini}{15pt}
    \setlength{\leftmarginii}{10pt}
    \newcommand{\tighthrule}{\hrulefill\vspace{-0.6em}}
    """ 

    return [
        "-V", "fontsize=10pt",
        "-V", f"header-includes={header_includes}"
    ]

def save_resume(resume: str, company_name: str, keep_md = False):
    save_md_to_pdf(resume, company_name, "resume", keep_md, get_resume_format_args())

if __name__ == "__main__":
    import os
    if os.path.exists("texts/job_info.txt"):
        with open("texts/job_info.txt", "r") as f:
            job_info = load_text("job_info")
    else:
        raise ValueError("No job info found, please run tailor.py first")

    llm = get_llm()
    job_d = parse_job_description(job_info, llm)

    result = make_resume(job_d)
    result = fix_resume_formatting(result)

    #save the file
    save_resume(result, job_d)