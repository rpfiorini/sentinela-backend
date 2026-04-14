from pydantic import BaseModel
from typing import Optional

class PersonCreate(BaseModel):
    kind: str
    name: str
    cargo: Optional[str] = None
    doc_id: Optional[str] = None
    phone: Optional[str] = None
    company_id: Optional[int] = None
