from langchain_groq import ChatGroq
import os

#get the model
model_name = os.getenv("LIGHT_MODEL_NAME")
api_key = os.getenv("GROQ_API_KEY")

def get_llm(temperature: int = 0) -> ChatGroq:
    return ChatGroq(model_name=model_name, api_key=api_key, temperature=temperature)