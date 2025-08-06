from pydantic import BaseModel, ValidationError
from dotenv import load_dotenv
import os

class BotConfig(BaseModel):
    token: str

def load_config():
    load_dotenv()
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    try:
        return BotConfig(token=token)
    except ValidationError as e:
        raise RuntimeError(f"Config validation error: {e}")

def get_llm_config():
    """Загружает конфиг LLM из .env."""
    return {
        "model": os.getenv("LLM_MODEL", "anthropic/claude-3.5-sonnet"),
        "temperature": float(os.getenv("LLM_TEMPERATURE", 0.7)),
        "max_tokens": int(os.getenv("LLM_MAX_TOKENS", 1000)),
    }

def get_openrouter_keys():
    """Загружает ключ и url OpenRouter из .env."""
    return {
        "api_key": os.getenv("OPENROUTER_API_KEY"),
        "base_url": os.getenv("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1")
    }

def get_system_prompt():
    """Загружает системный промпт из файла, путь берется из .env."""
    path = os.getenv("LLM_SYSTEM_PROMPT_PATH", "prompts/system_prompt.txt")
    with open(path, "r", encoding="utf-8") as f:
        return f.read().strip()