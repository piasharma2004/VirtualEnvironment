# src/my_package/settings.py
from dataclasses import dataclass

@dataclass
class AppConfig:
    openai_api_key: str
    openai_model: str = "gpt-4o-mini"
