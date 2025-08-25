from ai.tailor_projects import tailor_projects
from ai.parse_job_description import parse_job_description
from ai.llm_config import get_llm

import os
from dotenv import load_dotenv
from scraping.scrape_job_info import scrape_job_info
from util.text_util import load_text, save_text

load_dotenv()
link = os.getenv("TEST_JOB_LINK")

if os.path.exists("texts/job_info.txt"):
    with open("texts/job_info.txt", "r") as f:
        # job_info = f.read()
        job_info = load_text("job_info")
else:
    job_info = scrape_job_info(link)
    save_text(job_info, "job_info")

llm = get_llm()
job_d = parse_job_description(job_info, llm)
projects = tailor_projects(job_d, 4)

for project in projects:
    print("----")
    print(project.model_dump())