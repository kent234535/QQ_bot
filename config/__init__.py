"""
配置加载器 — 单例模式
从 data/*.json 加载配置，提供全局访问。
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .defaults import DEFAULT_PERSONAS, DEFAULT_PROVIDERS, DEFAULT_SETTINGS
from .settings import BotSettings

DATA_DIR = Path(__file__).resolve().parent.parent / "data"


def _ensure_data_dir() -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)


def _load_json(filename: str, default: Any) -> Any:
    _ensure_data_dir()
    path = DATA_DIR / filename
    if path.exists():
        return json.loads(path.read_text(encoding="utf-8"))
    # 首次运行：写入默认值
    _save_json(filename, default)
    return default


def _save_json(filename: str, data: Any) -> None:
    _ensure_data_dir()
    path = DATA_DIR / filename
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


class _ConfigManager:
    """全局配置管理器（单例）"""

    def __init__(self) -> None:
        self._settings: BotSettings | None = None
        self._personas: list[dict] | None = None
        self._providers: list[dict] | None = None

    # ── Settings ──

    @property
    def settings(self) -> BotSettings:
        if self._settings is None:
            raw = _load_json("settings.json", DEFAULT_SETTINGS)
            self._settings = BotSettings(**raw)
        return self._settings

    def save_settings(self, settings: BotSettings | None = None) -> None:
        if settings is not None:
            self._settings = settings
        if self._settings is not None:
            _save_json("settings.json", self._settings.model_dump())

    def update_settings(self, **kwargs: Any) -> BotSettings:
        current = self.settings.model_dump()
        current.update(kwargs)
        self._settings = BotSettings(**current)
        self.save_settings()
        return self._settings

    # ── Personas ──

    @property
    def personas(self) -> list[dict]:
        if self._personas is None:
            self._personas = _load_json("personas.json", DEFAULT_PERSONAS)
        return self._personas

    def get_persona(self, persona_id: str) -> dict | None:
        return next((p for p in self.personas if p["id"] == persona_id), None)

    def save_personas(self) -> None:
        _save_json("personas.json", self.personas)

    def add_persona(self, persona: dict) -> None:
        # 移除同 ID 旧记录
        self._personas = [p for p in self.personas if p["id"] != persona["id"]]
        self._personas.append(persona)
        self.save_personas()

    def delete_persona(self, persona_id: str) -> bool:
        before = len(self.personas)
        self._personas = [p for p in self.personas if p["id"] != persona_id]
        if len(self._personas) < before:
            self.save_personas()
            return True
        return False

    # ── Providers ──

    @property
    def providers(self) -> list[dict]:
        if self._providers is None:
            self._providers = _load_json("providers.json", DEFAULT_PROVIDERS)
        return self._providers

    def get_provider(self, provider_id: str) -> dict | None:
        return next((p for p in self.providers if p["id"] == provider_id), None)

    def get_active_provider(self) -> dict | None:
        pid = self.settings.active_provider_id
        if pid:
            return self.get_provider(pid)
        # 回退到第一个启用的 provider
        enabled = [p for p in self.providers if p.get("enabled", True)]
        return enabled[0] if enabled else None

    def save_providers(self) -> None:
        _save_json("providers.json", self.providers)

    def add_provider(self, provider: dict) -> None:
        self._providers = [p for p in self.providers if p["id"] != provider["id"]]
        self._providers.append(provider)
        self.save_providers()

    def delete_provider(self, provider_id: str) -> bool:
        before = len(self.providers)
        self._providers = [p for p in self.providers if p["id"] != provider_id]
        if len(self._providers) < before:
            self.save_providers()
            return True
        return False


# 全局单例
config = _ConfigManager()
