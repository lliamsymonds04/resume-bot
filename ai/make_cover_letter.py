from models.job_description import JobDescription
from ai.resume_util import get_input_data, remove_code_block


def make_cover_letter(input_data):
    input_data = get_input_data(job_description)

    
if __name__ == "__main__":
    with open("data/sample_job_description.txt", 'r', encoding='utf-8') as f:
        job_description_text = f.read()
    job_description = JobDescription(raw_text=job_description_text)
    input_data = get_input_data(job_description)
    cover_letter = make_cover_letter(input_data)
    print(cover_letter)

