import os
from dotenv import load_dotenv
from scraping.scrape_job_info import scrape_job_info
from util.text_util import save_text

load_dotenv()
link = os.getenv("TEST_JOB_LINK")

job_info = scrape_job_info(link)
save_text(job_info, "job_info.txt")