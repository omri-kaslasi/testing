
from pydantic import BaseModel, Field
from typing import Dict

class Source(BaseModel):
    id: str
    name: str
    type: str
    parse_vrl: str
    fields: list[str]
    key_fields: Dict[str, Dict[str, int]] = Field(default_factory=dict)
    frontend_port: int | None = None
