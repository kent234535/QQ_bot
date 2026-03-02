"""角色数据模型"""

from pydantic import BaseModel, Field


class Persona(BaseModel):
    """角色定义"""
    id: str = Field(..., description="唯一标识符")
    name: str = Field(..., description="显示名称")
    system_prompt: str = Field(..., description="角色描述")
    builtin: bool = Field(False, description="是否为内置角色")

    def to_dict(self) -> dict:
        return self.model_dump()

    @classmethod
    def from_dict(cls, data: dict) -> "Persona":
        return cls(**data)
