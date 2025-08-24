from langchain_groq import ChatGroq
import os

#get the model
model_name = os.getenv("MODEL_NAME")
api_key = os.getenv("GROQ_API_KEY")

llm = ChatGroq(model_name=model_name, api_key=api_key, temperature=0)