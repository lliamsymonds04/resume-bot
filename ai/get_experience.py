import json

def get_experience():
    with open("data/experience.json", 'r', encoding='utf-8') as f:
        experience = json.load(f)

    return experience

def generate_tailor_experience_prompt():
    return """
    You are an expert resume writer.
    Given the following job description, tailor the following experience to better match the job description.

    # Job Description:
    {job_description}

    # Experience:
    {experience}

    # Format instructions:
    {format_instructions}
    """

def tailor_experience(experience, job_description):
    # For simplicity, just return the experience as is.
    # In a real implementation, you would use AI to tailor this.
    return experience