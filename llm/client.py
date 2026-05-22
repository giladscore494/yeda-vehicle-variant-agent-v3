"""LLM client — calls the model. Stub-friendly for tests."""
from __future__ import annotations

from core.config import GEMINI_API_KEY, GEMINI_MODEL_STRONG


def call_model(prompt: str, model: str | None = None) -> str:
    """Call Gemini and return raw text response.

    Raises RuntimeError if API key is missing.
    """
    if not GEMINI_API_KEY:
        raise RuntimeError(
            "GEMINI_API_KEY is not configured. "
            "Set it in environment variables or secrets.py."
        )

    model_name = model or GEMINI_MODEL_STRONG

    from google import genai

    client = genai.Client(api_key=GEMINI_API_KEY)
    response = client.models.generate_content(
        model=model_name,
        contents=prompt,
    )
    return response.text
