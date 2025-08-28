from langchain_groq import ChatGroq
import os

#get the model
api_key = os.getenv("GROQ_API_KEY")

def get_llm(temperature: int = 0, model_type: str = "light") -> ChatGroq:
    if model_type == "light":
        model_name = os.getenv("LIGHT_MODEL_NAME")
    elif model_type == "good":
        model_name = os.getenv("GOOD_MODEL_NAME")
    else:
        raise ValueError("Invalid model type. Choose 'light' or 'good'.")

    return ChatGroq(model_name=model_name, api_key=api_key, temperature=temperature)