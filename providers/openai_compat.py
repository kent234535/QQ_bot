"""OpenAI 兼容适配器 — 覆盖阿里云百炼、DeepSeek、OpenRouter 等平台"""

from __future__ import annotations

import httpx

from .base import AIProvider


class OpenAICompatProvider(AIProvider):
    """OpenAI Chat Completions API 兼容适配器"""

    async def chat(
        self,
        messages: list[dict],
        *,
        max_tokens: int = 2000,
        temperature: float = 0.8,
        timeout: int = 120,
    ) -> str:
        url = f"{self.base_url.rstrip('/')}/chat/completions"

        async with httpx.AsyncClient(timeout=timeout) as client:
            resp = await client.post(
                url,
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json",
                },
                json={
                    "model": self.model,
                    "messages": messages,
                    "max_tokens": max_tokens,
                    "temperature": temperature,
                },
            )
            resp.raise_for_status()
            data = resp.json()
            return data["choices"][0]["message"]["content"]
