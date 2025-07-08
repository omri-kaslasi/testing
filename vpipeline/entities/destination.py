
from pydantic import BaseModel

class Destination(BaseModel):
    id: str
    name: str
    driver: str = 'vector_sink'
    endpoint: str = 'siem.local:514'
    credentials_ref: str | None = None
