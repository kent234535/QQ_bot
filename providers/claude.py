"""Anthropic Claude 适配器"""

from __future__ import annotations

import httpx

from .base import AIProvider


class ClaudeProvider(AIProvider):
    """Anthropic Messages API 适配器"""

    async def chat(
        self,
        messages: list[dict],
        *,
        max_tokens: int = 2000,
        temperature: float = 0.8,
        timeout: int = 120,
    ) -> str:
        # 分离 system prompt
        system_text = ""
        chat_messages = []
        for msg in messages:
            if msg["role"] == "system":
                system_text = msg["content"]
            else:
                chat_messages.append({"role": msg["role"], "content": msg["content"]})

        # 确保消息以 user 开头（Claude 要求）
        if chat_messages and chat_messages[0]["role"] != "user":
            chat_messages = [m for m in chat_messages if m["role"] != "assistant" or chat_messages.index(m) > 0]

        base = self.base_url.rstrip("/") if self.base_url else "https://api.anthropic.com"
        url = f"{base}/v1/messages"

        body: dict = {
            "model": self.model or "claude-sonnet-4-20250514",
            "max_tokens": max_tokens,
            "temperature": temperature,
            "messages": chat_messages,
        }
        if system_text:
            body["system"] = system_text

        async with httpx.AsyncClient(timeout=timeout) as client:
            resp = await client.post(
                url,
                headers={
                    "x-api-key": self.api_key,
                    "anthropic-version": "2023-06-01",
                    "Content-Type": "application/json",
                },
                json=body,
            )
            resp.raise_for_status()
            data = resp.json()
            # Claude 返回格式: {"content": [{"type": "text", "text": "..."}]}
            return data["content"][0]["text"]
