from util.text_util import load_text, save_text
from ai.llm_config import get_llm
from ai.parse_job_description import parse_job_description
from scraping.get_jobs import get_jobs
from ai.parse_job_listings import parse_job_listings
import os

from dotenv import load_dotenv
load_dotenv()

# job_description = load_text("job_info")
# if not job_description:
#     raise ValueError("Job description is empty or could not be loaded")

# llm = get_llm()
# parsed_job = parse_job_description(job_description, llm)

# print(parsed_job.model_dump())

#check if texts/jobs.text exists
if os.path.exists("texts/jobs.txt"):
    print("loaded from texts/jobs.txt")
    jobs = load_text("jobs")
else:
    jobs = get_jobs()
    save_text(jobs, "jobs")

job_listings = parse_job_listings(jobs)
for job in job_listings.jobs:
    print(job.model_dump())