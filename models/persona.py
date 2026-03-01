"""人格数据模型"""

from pydantic import BaseModel, Field


class Persona(BaseModel):
    """人格定义"""
    id: str = Field(..., description="唯一标识符")
    name: str = Field(..., description="显示名称")
    system_prompt: str = Field(..., description="系统提示词")
    description: str = Field("", description="人格描述")
    builtin: bool = Field(False, description="是否为内置人格（不可删除）")

    def to_dict(self) -> dict:
        return self.model_dump()

    @classmethod
    def from_dict(cls, data: dict) -> "Persona":
        return cls(**data)
