import os
from langchain_groq import ChatGroq

def groq_models(model_name: str, kwargs):
    
    return ChatGroq(
        model = model_name,
        temperature = kwargs.get("temperature", 1.0),
        max_tokens = kwargs.get("max_tokens", 3000),
        timeout = None,
        max_retries = kwargs.get("max_retries", 2)
        # other params...
    )

def get_model(provider_prefix: str, model_name: str, **kwargs):
    if provider_prefix == 'groq':
        return groq_models(model_name, kwargs)
    
    raise "Unknown provider"