"""AI 提供商抽象基类"""

from __future__ import annotations

from abc import ABC, abstractmethod


class AIProvider(ABC):
    """所有 AI 提供商的基类"""

    def __init__(self, config: dict) -> None:
        self.config = config
        self.api_key: str = config.get("api_key", "")
        self.base_url: str = config.get("base_url", "")
        self.model: str = config.get("model", "")

    @abstractmethod
    async def chat(
        self,
        messages: list[dict],
        *,
        max_tokens: int = 2000,
        temperature: float = 0.8,
        timeout: int = 120,
    ) -> str:
        """
        发送聊天请求，返回助手回复文本。
        messages: OpenAI 格式的消息列表 [{role, content}, ...]
        """
        ...

    @property
    def name(self) -> str:
        return self.config.get("name", self.__class__.__name__)

    @property
    def provider_id(self) -> str:
        return self.config.get("id", "")
