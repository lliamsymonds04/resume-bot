import json
from models.job_description import JobDescription
from langchain_core.documents import Document
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

def tailor_projects(job_description: JobDescription, num_projects: int = 3):
    #load the projects json
    with open("data/projects.json", "r") as f:
        projects_data = json.load(f)

    project_docs = []
    for project in projects_data:
        # Combine title and description for better matching
        content = f"Title: {project['title']}\nDescription: {project['description']}"
        # Store the full project data in metadata
        doc = Document(page_content=content, metadata=project)
        project_docs.append(doc)

    # embeddings = OpenAIEmbeddings()
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    vs = FAISS.from_documents(project_docs, embeddings)

    prompt = f"""
    Based on the following job description, find the most relevant projects:
    {job_description.model_dump()}

    Here are the top {num_projects} projects:
    """

    retrieved_docs = vs.similarity_search(prompt, k=num_projects)

    for doc in retrieved_docs:
        print(f"Title: {doc.metadata['title']}")
        print(f"Description: {doc.metadata['description']}")
        print()