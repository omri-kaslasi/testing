
from pydantic import BaseModel
from tomlkit import TOMLDocument

class VectorConfig(BaseModel):
    name: str
    document: TOMLDocument
    path: str
