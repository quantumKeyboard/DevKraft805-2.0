"""
ai/ollama_client.py
Wrapper for the Ollama HTTP API.
Handles retries, timeouts, and a clean interface for all AI calls in the project.
"""

import json
import logging
import time
import httpx

from core.config import get_settings

logger = logging.getLogger(__name__)


class OllamaError(Exception):
    """Raised when Ollama cannot fulfil a request after all retries."""


def call_ollama(
    prompt: str,
    system_prompt: str = "",
    max_tokens: int = 512,
    model: str = "",
    timeout: int = 0,
    retries: int = -1,
) -> str:
    """
    Make a synchronous call to the local Ollama API.

    Args:
        prompt:        The user prompt.
        system_prompt: Optional system prompt.
        max_tokens:    Max tokens in the response (passed as num_predict).
        model:         Override the model from config.
        timeout:       Override timeout (seconds) from config.
        retries:       Override retry count from config.

    Returns:
        The generated text string.

    Raises:
        OllamaError: if the call fails after all retries.
    """
    settings = get_settings()
    model = model or settings.ollama_model
    timeout = timeout or settings.ollama_timeout
    retries = retries if retries >= 0 else settings.ollama_max_retries
    base_url = settings.ollama_base_url.rstrip("/")

    payload: dict = {
        "model": model,
        "prompt": prompt,
        "stream": False,
        "options": {
            "num_predict": max_tokens,
            "temperature": 0.3,
        },
    }
    if system_prompt:
        payload["system"] = system_prompt

    url = f"{base_url}/api/generate"
    last_error: Exception | None = None

    for attempt in range(retries + 1):
        try:
            with httpx.Client(timeout=timeout) as client:
                response = client.post(url, json=payload)
                response.raise_for_status()
                data = response.json()
                return data.get("response", "").strip()

        except httpx.TimeoutException as exc:
            last_error = exc
            logger.warning(
                f"Ollama timeout on attempt {attempt + 1}/{retries + 1}. "
                f"Retrying..." if attempt < retries else "No more retries."
            )
            if attempt < retries:
                time.sleep(1)

        except httpx.HTTPStatusError as exc:
            last_error = exc
            logger.error(f"Ollama HTTP error {exc.response.status_code}: {exc.response.text}")
            break  # Don't retry on HTTP errors

        except Exception as exc:
            last_error = exc
            logger.error(f"Unexpected Ollama error: {exc}")
            if attempt < retries:
                time.sleep(1)

    raise OllamaError(
        f"Ollama call failed after {retries + 1} attempt(s): {last_error}"
    )


def is_ollama_available() -> bool:
    """Quick health-check: returns True if Ollama is running and reachable."""
    settings = get_settings()
    try:
        with httpx.Client(timeout=5.0) as client:
            response = client.get(f"{settings.ollama_base_url}/api/tags")
            return response.status_code == 200
    except Exception:
        return False


def list_available_models() -> list[str]:
    """Returns the list of locally pulled Ollama models."""
    settings = get_settings()
    try:
        with httpx.Client(timeout=5.0) as client:
            response = client.get(f"{settings.ollama_base_url}/api/tags")
            data = response.json()
            return [m["name"] for m in data.get("models", [])]
    except Exception:
        return []
