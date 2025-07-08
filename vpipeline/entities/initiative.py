
from pydantic import BaseModel

class OptimizationInitiative(BaseModel):
    id: str
    name: str
    description: str
    data_source: str
    vrl: str
    relevancy_rule: str
