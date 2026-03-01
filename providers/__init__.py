"""AI 提供商工厂 + 注册"""

from __future__ import annotations

from .base import AIProvider
from .openai_compat import OpenAICompatProvider
from .claude import ClaudeProvider

_REGISTRY: dict[str, type[AIProvider]] = {
    "openai_compat": OpenAICompatProvider,
    "claude": ClaudeProvider,
}


def create_provider(provider_config: dict) -> AIProvider:
    """根据配置创建 AI 提供商实例"""
    provider_type = provider_config.get("type", "openai_compat")
    cls = _REGISTRY.get(provider_type)
    if cls is None:
        raise ValueError(f"未知的提供商类型: {provider_type}")
    return cls(provider_config)


__all__ = ["AIProvider", "OpenAICompatProvider", "ClaudeProvider", "create_provider"]
