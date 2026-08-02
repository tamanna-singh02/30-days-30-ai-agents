from typing import Any
from langchain_core.language_models import BaseChatModel

from shared.config import (
    MODEL_NAME,
    MODEL_PROVIDER,
    TEMPERATURE,
    GROQ_API_KEY,
    OPENAI_API_KEY,
    ANTHROPIC_API_KEY,
    GOOGLE_API_KEY,
)
from shared.logger import logger

def get_llm(
    provider: str = MODEL_PROVIDER,
    model: str = MODEL_NAME,
    temperature: float = TEMPERATURE,
    **kwargs: Any,
) -> BaseChatModel:
    """
    Factory function to initialize LLM provider models (Groq, OpenAI, Anthropic, Google Gemini).
    """
    provider_lower = provider.lower()

    if provider_lower == "groq":
        from langchain_groq import ChatGroq
        return ChatGroq(
            model=model or "llama-3.3-70b-versatile",
            temperature=temperature,
            groq_api_key=GROQ_API_KEY or None,
            **kwargs,
        )
    elif provider_lower == "openai":
        from langchain_openai import ChatOpenAI
        return ChatOpenAI(
            model=model or "gpt-4o-mini",
            temperature=temperature,
            api_key=OPENAI_API_KEY or None,
            **kwargs,
        )
    elif provider_lower == "anthropic":
        from langchain_anthropic import ChatAnthropic
        return ChatAnthropic(
            model=model or "claude-3-5-sonnet-20240620",
            temperature=temperature,
            api_key=ANTHROPIC_API_KEY or None,
            **kwargs,
        )
    elif provider_lower == "google" or provider_lower == "gemini":
        from langchain_google_genai import ChatGoogleGenerativeAI
        return ChatGoogleGenerativeAI(
            model=model or "gemini-1.5-flash",
            temperature=temperature,
            google_api_key=GOOGLE_API_KEY or None,
            **kwargs,
        )
    else:
        logger.warning(f"Unknown provider '{provider}'. Defaulting to ChatGroq.")
        from langchain_groq import ChatGroq
        return ChatGroq(
            model=model or "llama-3.3-70b-versatile",
            temperature=temperature,
            groq_api_key=GROQ_API_KEY or None,
            **kwargs,
        )
