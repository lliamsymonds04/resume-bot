from util.text_util import load_text
from ai.llm_config import get_llm
from ai.parse_job_description import parse_job_description

job_description = load_text("job_info")
if not job_description:
    raise ValueError("Job description is empty or could not be loaded")

llm = get_llm()
parsed_job = parse_job_description(job_description, llm)

print(parsed_job.model_dump())