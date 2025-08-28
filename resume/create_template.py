from langchain_groq import ChatGroq
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

import os

#get the model
model_name = os.getenv("GOOD_MODEL_NAME")
api_key = os.getenv("GROQ_API_KEY")

def create_resume_template(header_elements: list[str], sections: list[str]):
    llm = ChatGroq(model_name=model_name, api_key=api_key, temperature=0)

    full_prompt = ChatPromptTemplate.from_template(f"""
        Generate a complete, single-page resume template in the Typst markup language. The template must be optimized for Applicant Tracking Systems (ATS).

        **Template Requirements:**
        - The resume must not exceed one page.
        - Use clear, professional typography.
        - All sections should be structured for easy parsing by ATS.
        - Include the following header elements, separated by the pipe character (|) on a single line: {', '.join(header_elements)}
        - The template must contain the following sections, in this order: {', '.join(sections)}
        - Use Typst's markup syntax correctly, including show rules for formatting.
        - Ensure there are no syntax errors and the code is well-structured.
        - Provide only the Typst code and nothing else.
    """)

    # Construct the correct chain
    resume_chain = full_prompt | llm | StrOutputParser()

    result = resume_chain.invoke({'header_elements': header_elements, 'sections': sections})
    return result


def save_typst_template(template_content: str, filename: str = "resume_template.typ"):
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(template_content)
    print(f"Template saved to {filename}")
    return filename