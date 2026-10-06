"""
course_llm.py — общий слой доступа к LLM для всех лабораторных курса.

Контракт один на весь курс:  backend.chat(messages) -> str
где messages = [{"role": "system"|"user"|"assistant", "content": "..."}].

Использование в ноутбуке (ячейка):
    import sys; sys.path.append("..")        # labs/ на пути
    from course_llm import MockLLM, OpenAIBackend, AnthropicBackend

    llm = MockLLM(scripted=[...])             # оффлайн, без ключей
    # llm = OpenAIBackend(model="gpt-4o-mini")
    # llm = OpenAIBackend(model="qwen2.5", base_url="http://localhost:11434/v1")  # локальный Ollama
    # llm = AnthropicBackend(model="claude-3-5-haiku-latest")

Бэкенды импортируют SDK ЛЕНИВО (внутри __init__), поэтому модуль грузится без openai/anthropic.
"""
from __future__ import annotations

from openai import OpenAI
import anthropic


class MockLLM:
    """Оффлайн-заглушка. Возвращает заранее заданный список ответов по очереди.
    Нужна, чтобы отладить логику цикла без ключей и сети. Конкретный сценарий
    (scripted) задаётся в каждой ЛР под её задачу."""
    name = "mock"

    def __init__(self, scripted=None):
        self.scripted = list(scripted or ["(mock ответа нет — задайте scripted=[...])"])
        self.i = 0

    def chat(self, messages):
        out = self.scripted[min(self.i, len(self.scripted) - 1)]
        self.i += 1
        return out


class OpenAIBackend:
    """OpenAI-совместимый бэкенд. base_url можно указать на локальный Ollama/LM Studio."""
    def __init__(self, model="gpt-4o-mini", base_url=None, temperature=0):
        self.client = OpenAI(base_url=base_url) if base_url else OpenAI()
        self.model = model
        self.temperature = temperature
        self.name = f"openai:{model}"

    def chat(self, messages):
        r = self.client.chat.completions.create(
            model=self.model, messages=messages, temperature=self.temperature)
        return r.choices[0].message.content


class AnthropicBackend:
    """Claude. Системные сообщения собираются в параметр system."""
    def __init__(self, model="claude-3-5-haiku-latest", max_tokens=1024, temperature=0):
        self.client = anthropic.Anthropic()
        self.model = model
        self.max_tokens = max_tokens
        self.temperature = temperature
        self.name = f"anthropic:{model}"

    def chat(self, messages):
        system = "\n".join(m["content"] for m in messages if m["role"] == "system")
        conv = [m for m in messages if m["role"] != "system"]
        r = self.client.messages.create(
            model=self.model, system=system, messages=conv,
            max_tokens=self.max_tokens, temperature=self.temperature)
        return r.content[0].text


__all__ = ["MockLLM", "OpenAIBackend", "AnthropicBackend"]
