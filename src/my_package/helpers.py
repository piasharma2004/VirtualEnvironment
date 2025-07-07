# src/my_package/helpers.py
import os
from dotenv import load_dotenv
from settings import AppConfig

def load_config() -> AppConfig:
    load_dotenv()
    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:
        raise ValueError("Missing OPENAI_API_KEY in environment variables.")

    return AppConfig(openai_api_key=api_key.strip())

