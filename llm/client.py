from openai import OpenAI
from typing import List, Dict
import structlog
import time

logger = structlog.get_logger()

def create_client(api_key: str, base_url: str) -> OpenAI:
    """Создает OpenAI клиент для OpenRouter."""
    return OpenAI(api_key=api_key, base_url=base_url, timeout=30)


def format_messages(history: List[Dict], user_message: str, system_prompt: str) -> List[Dict]:
    """Формирует список сообщений для OpenAI API."""
    messages = [{"role": "system", "content": system_prompt}]
    messages.extend(history)
    messages.append({"role": "user", "content": user_message})
    return messages[-6:]  # максимум 5 + system


def generate_response(client: OpenAI, messages: List[Dict], config: dict) -> str:
    """Отправляет запрос к LLM и возвращает ответ. Логирует статистику."""
    start = time.time()
    try:
        logger.debug("llm_request", model=config["model"], messages=messages)
        response = client.chat.completions.create(
            model=config["model"],
            messages=messages,
            temperature=config["temperature"],
            max_tokens=config["max_tokens"]
        )
        elapsed = int((time.time() - start) * 1000)
        tokens_in = response.usage.prompt_tokens if hasattr(response, "usage") else None
        tokens_out = response.usage.completion_tokens if hasattr(response, "usage") else None
        logger.info(
            "llm_response",
            model=config["model"],
            tokens_in=tokens_in,
            tokens_out=tokens_out,
            response_time_ms=elapsed,
            status="success"
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        elapsed = int((time.time() - start) * 1000)
        logger.error(
            "llm_error",
            error=str(e),
            response_time_ms=elapsed,
            status="error"
        )
        raise RuntimeError(f"LLM error: {e}")
