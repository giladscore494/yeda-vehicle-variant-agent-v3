"""LLM client — calls the model. Stub-friendly for tests."""
from __future__ import annotations

from core.config import GEMINI_API_KEY, GEMINI_MODEL_STRONG


def call_model(
    prompt: str,
    model: str | None = None,
    use_google_search: bool = False,
) -> str:
    """Call Gemini and return raw text response.

    Args:
        prompt: The text prompt to send to the model.
        model: Override the default model ID.
        use_google_search: When True, enables the Google Search grounding tool.
            The tool is passed via ``config=types.GenerateContentConfig(tools=[…])``
            — never as a top-level keyword — to comply with the SDK contract.

    Raises:
        RuntimeError: If GEMINI_API_KEY is not configured.
    """
    if not GEMINI_API_KEY:
        raise RuntimeError(
            "GEMINI_API_KEY is not configured. "
            "Set it in environment variables or secrets.py."
        )

    model_name = model or GEMINI_MODEL_STRONG

    from google import genai
    from google.genai import types

    client = genai.Client(api_key=GEMINI_API_KEY)

    if use_google_search:
        config = types.GenerateContentConfig(
            tools=[types.Tool(google_search=types.GoogleSearch())]
        )
        response = client.models.generate_content(
            model=model_name,
            contents=prompt,
            config=config,
        )
    else:
        response = client.models.generate_content(
            model=model_name,
            contents=prompt,
        )

    return response.text

