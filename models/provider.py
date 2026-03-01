"""AI 提供商数据模型"""

from pydantic import BaseModel, Field


class ProviderConfig(BaseModel):
    """AI 提供商配置"""
    id: str = Field(..., description="唯一标识符")
    name: str = Field(..., description="显示名称")
    type: str = Field(..., description="适配器类型: openai_compat | claude")
    base_url: str = Field("", description="API Base URL")
    api_key: str = Field("", description="API Key")
    model: str = Field("", description="模型名称")
    enabled: bool = Field(True, description="是否启用")

    def to_dict(self) -> dict:
        return self.model_dump()

    @classmethod
    def from_dict(cls, data: dict) -> "ProviderConfig":
        return cls(**data)
