from ai.resume_util import get_md_path, get_output_path, save_pdf
from make_resume import get_resume_format_args
import os


if __name__ == "__main__":
    job_name = input("Enter the company name for relinting: ").strip()
    output_path = get_output_path(job_name) 

    # First try to relint the resume
    tail_name = "resume"
    md_file_path = get_md_path(output_path["base_path"], tail_name)
    #check the markdown exists
    if not os.path.exists(md_file_path):
        raise FileNotFoundError(f"Markdown file not found: {md_file_path}")
    save_pdf(md_file_path, output_path["base_path"], output_path["user_name"], tail_name, get_resume_format_args())